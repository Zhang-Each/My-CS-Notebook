# VAE与CVAE的基本架构
## VAE与CVAE的基本架构
> 简单了解一下VAE的设计思路，首先补充一些熟悉的概率论知识，然后记录一下VAE的原论文中涉及到的一些关键的推导和结论。
### 1. 一些概率论的基本常识
#### 1.1 后验概率
后验概率是在观察到一些数据或证据之后，对于一个模型参数或假设的概率分布。换句话说，后验概率是给定数据或证据的条件下，模型参数或假设的不确定性的度量。在贝叶斯统计学中，我们通常将参数或假设视为随机变量，因此它们的分布可以表示为概率分布。当我们观察到新的数据时，我们可以使用贝叶斯定理来更新我们对模型参数或假设的先验信念，从而获得后验概率分布。
> 注：这段话来自于ChatGPT，更简单地说，后验概率就是给定数据x时候它的标签y的条件分布，而先验概率则是给定标签y的时候x的条件分布。


#### 1.2 极大似然估计
极大似然估计（Maximum Likelihood Estimation，简称MLE）是一种常用的参数估计方法，它的基本思想是寻找最有可能导致观测数据出现的模型参数值。
当假设数据样本独立同分布时，极大似然估计可以表示为最大化似然函数的形式。假设我们有一个参数化的概率分布 $p(x;\theta)$，其中 $x$ 是观测数据，$\theta$ 是模型参数。给定一个样本集合 $\mathcal{D}={x_1,x_2,...,x_n}$，样本独立同分布于分布 $p(x;\theta)$。则似然函数可以表示为：

$$
L(\theta \mid \mathcal{D})=p(\mathcal{D} \mid \theta)=\prod_{i=1}^n p\left(x_i ; \theta\right)
$$

极大似然估计的目标是最大化似然函数，即找到最优的参数 $\theta$ 使得似然函数取得最大值，这个目标可以表示为：

$$
\theta_{MLE}=\arg\max L(\theta \mid \mathcal{D})=\arg\max \prod_{i=1}^n p\left(x_i ; \theta\right)
$$

通常为了避免出现下溢的问题，会对似然函数取对数，这样极大化对数似然函数等价于极大化似然函数，也就是说：

$$
\begin{aligned}
\theta_{MLE}&=\arg\max \log L(\theta \mid \mathcal{D})
\\&=\arg\max \sum_{i=1}^n \log p\left(x_i ; \theta\right)
\end{aligned}
$$

### 1.3 后验概率最大化估计
Maximum a posteriori (MAP)算法是一种用于估计参数的统计方法，它结合了先验概率和似然函数来计算后验概率。在贝叶斯推断中，MAP算法用于估计最有可能的参数值，即在给定观测数据的情况下，使得后验概率最大的参数值。

和最大似然估计一样，MAP算法也是一种参数估计方法，但不同的是，它引入了先验概率。先验概率是参数在观测数据之前的概率分布，它反映了我们对参数的先前知识。通过引入先验概率，我们可以**避免在数据样本较小的情况下过拟合**，同时也可以对参数进行正则化。MAP公式可以表示为：

$$
\theta_{MAP} = \underset{\theta}{\arg\max}\ p(\theta | D) = \underset{\theta}{\arg\max}\ p(D|\theta)p(\theta)
$$
其中，$\theta_{\text{MAP}}$ 是最大化后验概率 $p(\theta | D)$ 时对应的参数值，$D$ 是观测数据，$p(D|\theta)$ 是似然函数，$p(\theta)$ 是先验概率。**最大后验概率估计是最大似然和贝叶斯估计的结合**，相比于极大似然估计，它在目标中加入了对参数的先验。


## 2. VAE
VAE的原论文🔗：[Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114)
论文对生成任务的场景做了这样的定义，首先给定一个独立同分布的数据集$\mathbf{X}=\left\{\mathbf{x}^{(i)}\right\}_{i=1}^N$ 并且其中的每一条数据$\mathbf{x}^{(i)}$是一个从随机过程中产生的连续或者离散的数据，并且生成的过程中包含了一个未观测到的随机变量$\mathbf{z}$，我们进一步假设，这个生成的过程可以分成这样两个步骤：
1. 从概率分布$p_{\boldsymbol{\theta}^*}(\mathbf{z})$中生成一个值$\mathbf{z}^{i}$
2. 根据给定的值$\mathbf{z}^{i}$生成条件概率$P(\mathbf{x}^{(i)}|\mathbf{z}^{(i)})$ 
现在的问题在于，我们既不知道$\mathbf{z}$的分布情况，也不知道参数$\theta^*$，这是一个通用的生成算法框架，我们没有对变量的分布情况作出任何假设，但是，这个算法会碰到这样两个问题：
1. Intractability，有的时候计算似然$P(\mathbf{x})$的分布会非常麻烦，甚至无法计算(比如图像生成中，我们很难计算这个似然)，这就导致我们不能用贝叶斯公式计算后验概率，所以EM算法也无法使用，各种变分贝叶斯算法也无法使用(虽然我不知道变分贝叶斯是什么东西)
2. Scalability，当数据集非常大的时候，我们不能进行full-batch的优化，只能用一些mini-batch来不断更新参数，像是蒙特卡洛EM这样的基于采样的算法这就对算法的可靠性提出了挑战。
这篇论文提出的变分自编码器(VAE)框架，就是为了解决这样几个问题：
1. 对参数$\mathbf{\theta}$进行有效的近似ML或MAP估计。
2. 对于给定的数据点$\mathbf{x}^{(i)}$生成合适的隐变量$\mathbf{z}$，这可以用于数据表示和压缩编码
3. 对变量$\mathbf{x}$进行有效的近似边际推断

为了达到这样的目的，VAE引入一个识别模型$q_{\phi}(\mathbf{z}|\mathbf{x})$作为概率编码器，对输入的数据x进行编码，用$\mathbf{z}$来作为x的编码表示，然后使用一个概率解码器$p_{\theta}(\mathbf{z}|\mathbf{x})$将编码表示转换为原本的值。我们只要学到了一个足够好的解码器，就可以从$\mathbf{z}$的分布中随机采样出合适的一个值，然后就可以生成合适的$\mathbf{x}$，这样一来，我们就得到了一个可以使用的生成器。

同时，数据集上的边际似然可以表示为：

$$
\log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(1)}, \cdots, \mathbf{x}^{(N)}\right)=\sum_{i=1}^N \log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(i)}\right)
$$

对于每一个单独的数据点$\mathbf{x}$，我们有：

$$
\log p_{\boldsymbol{\theta}}\left(\mathbf{x}\right)=D_{K L}\left(q_{\boldsymbol{\phi}}\left(\mathbf{z} \mid \mathbf{x}\right) \| p_{\boldsymbol{\theta}}\left(\mathbf{z} \mid \mathbf{x}\right)\right)+\mathcal{L}\left(\boldsymbol{\theta}, \boldsymbol{\phi} ; \mathbf{x}\right)
$$

这一步的推导过程如下，对于一个数据点$\mathbf{x}$，我们有：

$$
\begin{aligned}
\log p_{\theta}(\mathbf{x})&=\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log p_{\theta}(\mathbf{x}) \mathrm{d}z
\\&=\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log \frac{p_{\theta}(\mathbf{x}|\mathbf{z})p_{\theta}(\mathbf{z})q_{\phi}(\mathbf{z}|\mathbf{x})}{p_{\theta}(\mathbf{z}|\mathbf{x})q_{\phi}(\mathbf{z}|\mathbf{x})} \mathrm{d}z
\\&=\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log \frac{p_{\theta}(\mathbf{x}|\mathbf{z})p_{\theta}(\mathbf{z})}{q_{\phi}(\mathbf{z}|\mathbf{x})} \mathrm{d}z+\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log \frac{q_{\phi}(\mathbf{z}|\mathbf{x})}{p_{\theta}(\mathbf{z}|\mathbf{x})} \mathrm{d}z
\\&=\mathcal{L}(\theta,\phi,\mathbf{x})+D_{KL}(q_{\phi}\left(\mathbf{z}|\mathbf{x})||p_{\theta}(\mathbf{z}|\mathbf{x})\right)
\end{aligned}
$$


这里面的$\mathcal{L}(\theta,\phi,\mathbf{x})$就是变分下界(variationallower bound)，它还可以做进一步的变形：

$$
\begin{aligned}
\mathcal{L}(\theta,\phi,\mathbf{x})&=\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log \frac{p_{\theta}(\mathbf{x}|\mathbf{z})p_{\theta}(\mathbf{z})}{q_{\phi}(\mathbf{z}|\mathbf{x})} \mathrm{d}z\\
&=\mathbb{E}_{q_{\boldsymbol{\phi}}(\mathbf{z} \mid \mathbf{x})}\left[-\log q_{\boldsymbol{\phi}}(\mathbf{z} \mid \mathbf{x})+\log p_{\boldsymbol{\theta}}(\mathbf{x}, \mathbf{z})\right]
\end{aligned}
$$

也可以写成是：

$$
\begin{aligned}
\mathcal{L}(\theta,\phi,\mathbf{x})&=\int_{z}q_{\phi}(\mathbf{z}|\mathbf{x})\log \frac{p_{\theta}(\mathbf{x}|\mathbf{z})p_{\theta}(\mathbf{z})}{q_{\phi}(\mathbf{z}|\mathbf{x})} \mathrm{d}z\\&=
-D_{K L}\left(q_{\boldsymbol{\phi}}\left(\mathbf{z} \mid \mathbf{x}^{(i)}\right) \| p_{\boldsymbol{\theta}}(\mathbf{z})\right)+\mathbb{E}_{q_{\boldsymbol{\phi}}\left(\mathbf{z} \mid \mathbf{x}^{(i)}\right)}\left[\log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(i)} \mid \mathbf{z}\right)\right]
\end{aligned}
$$


两种变形方式其实是等价的，我们的优化目标就变成了这个lower bound，自习观察可以发现，这个lower bound的第一项是一个**KL散度**(让编码器生成的z的条件分布和解码器中z的分布尽可能相似)，其实可以看成是一个正则项。而第二项则是一个**重构损失**(将x编码成z后再还原回x)，这两者一结合，其实就是VAE的设计目标对上了。论文中给出了两种方法来优化这个lower bound：
第一种方法Stochastic Gradient Variational Bayes (SGVB)通过蒙特卡洛方法来估计这个下界，具体的操作是：

$$
\begin{array}{l}
\widetilde{\mathcal{L}}^A\left(\boldsymbol{\theta}, \boldsymbol{\phi} ; \mathbf{x}^{(i)}\right)=\frac{1}{L} \sum_{l=1}^L \log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(i)}, \mathbf{z}^{(i, l)}\right)-\log q_{\boldsymbol{\phi}}\left(\mathbf{z}^{(i, l)} \mid \mathbf{x}^{(i)}\right) \\
\text { where } \quad \mathbf{z}^{(i, l)}=g_{\boldsymbol{\phi}}\left(\boldsymbol{\epsilon}^{(i, l)}, \mathbf{x}^{(i)}\right) \quad \text { and } \quad \boldsymbol{\epsilon}^{(l)} \sim p(\boldsymbol{\epsilon})
\end{array}
$$

第二种估计方法把KL散度保留了下来，因为这个项可以通过假设化简出来，而后面的这个重构期望才是需要估计的，具体的估计方法是：

$$
\widetilde{\mathcal{L}}^B\left(\boldsymbol{\theta}, \boldsymbol{\phi} ; \mathbf{x}^{(i)}\right)=-D_{K L}\left(q_{\boldsymbol{\phi}}\left(\mathbf{z} \mid \mathbf{x}^{(i)}\right) \| p_{\boldsymbol{\theta}}(\mathbf{z})\right)+\frac{1}{L} \sum_{l=1}^L\left(\log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(i)} \mid \mathbf{z}^{(i, l)}\right)\right)
$$

VAE模型在训练的过程中，我们需要先把输入的x编码成条件分布$P(\mathbf{z}|\mathbf{x})$然后从里面采样一个$\mathbf{z}$出来进行解码，但是这个采样的过程会导致梯度无法回传，因此论文中使用了一个重参数化技巧： 
> 从一个正态分布$\mathcal{N}(\mu, \sigma^2)$中采样一个$z$，相当于从标准正态分布$\mathcal{N}(0, 1)$中采样一个$\epsilon$然后计算出$z=\mu+\epsilon\sigma$

而在具体实现的时候，作者使用了MLP作为编码器，来预测每个数据点$\mathbf{x}$对应的正态的期望和方差，并假设$p_{\theta}(\mathbf{z})$是一个标准正态分布，编码器对每个数据点$\mathbf{x}$的编码结果$\mathbf{z}$的分布也是正态分布，所以我们有：

$$
\log q_{\boldsymbol{\phi}}\left(\mathbf{z} \mid \mathbf{x}^{(i)}\right)=\log \mathcal{N}\left(\mathbf{z} ; \boldsymbol{\mu}^{(i)}, \boldsymbol{\sigma}^{2(i)} \mathbf{I}\right)
$$


这样一来，训练目标中的KL散度也就可以计算了，因为KL散度中的两个分布都是高斯分布，反正最终计算的结果变成了：

$$
\mathcal{L}\left(\boldsymbol{\theta}, \boldsymbol{\phi} ; \mathbf{x}^{(i)}\right)=\frac {1}{2}\sum_{i=1}^{J}\left(1+\log (\sigma_j^{(i)})^2-(\mu_{j}^{(i)})^2-(\sigma_j^{(i)})^2\right)+\frac{1}{L} \sum_{l=1}^L\left(\log p_{\boldsymbol{\theta}}\left(\mathbf{x}^{(i)} \mid \mathbf{z}^{(i, l)}\right)\right)
$$


其中$\mathbf{z}^{(i, l)}=\boldsymbol{\mu}^{(i)}+\boldsymbol{\sigma}^{(i)} \odot \boldsymbol{\epsilon}^{(l)}$是重参数化后采样得到的噪声。这样一来，整个模型的基本架构就介绍完了，我们就可以训练VAE模型了。同时，VAE作为一个通用的框架，给我们留下了很多设计空间，比如编码器和解码器的具体选择，以及噪声z所服从的分布的假设等等，我们可以根据实际需要，设计出多种多样的VAE模型。

## 3. Conditional-VAE
原论文🔗：[Learning Structured Output Representation using Deep Conditional Generative Models](https://papers.nips.cc/paper/2015/file/8d55a249e6baa5c06772297520da2051-Paper.pdf)
Conditional-VAE是VAE的一个改进，它可以实现可控的生成，不过总的改进其实不多，我们假设$\mathbf{x},\mathbf{y},\mathbf{z}$分别是生成器的输入变量(也就是数据的某种特征)，待生成的变量和中间隐层变量，那么C-VAE的训练目标可以表示为：

$$
\widetilde{\mathcal{L}}_{\mathrm{CVAE}}(\mathbf{x}, \mathbf{y} ; \theta, \phi)=-K L\left(q_\phi(\mathbf{z} \mid \mathbf{x}, \mathbf{y}) \| p_\theta(\mathbf{z} \mid \mathbf{x})\right)+\frac{1}{L} \sum_{l=1}^L \log p_\theta\left(\mathbf{y} \mid \mathbf{x}, \mathbf{z}^{(l)}\right)
$$

简单来说，就是我们输入$\mathbf{x},\mathbf{y}$并编码得到$\mathbf{z}$，然后通过$\mathbf{x},\mathbf{z}$来重构$\mathbf{y}$，同时我们希望编码器得到的噪声分布，~~其实就是改了一下编码器和解码器的网络架构~~。

