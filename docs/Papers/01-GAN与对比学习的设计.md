# GAN中对比学习模块的设计

这里主要记录一些GAN+对比学习的论文的核心设计与idea中蕴含的想法(也就是他们讲的故事)，来简单学习一下GAN+对比学习要怎么讲出故事。

## 1. Infomax-GAN 
> 原论文：[InfoMax-GAN: Improved Adversarial Image Generation via Information Maximization and Contrastive Learning](https://arxiv.org/abs/2007.04589) 发表于CVPR2021

这篇论文是提出了用互信息最大化和对比学习的方式来提升图像生成的质量。事实上互信息是信息论中的一个概念，互信息最大化的目标如下：

$$
\max_{E \in \mathcal{E}} \mathcal{I}(X ; E(X))
$$

其中$\mathcal{I}$ 是互信息的计算函数，X是原本的数据，而E则是一个编码器，也就是说，我们要最大化**原本数据和编码器得到的表示之间的互信息**，但是原本数据的分布实际上难以测定，因此这个目标又可以修改成：

$$
\max_{E \in \mathcal{E}} \mathcal{I}(C_{\phi}(X) ; E_{\phi}(X))
$$

其中C和E是在相同参数$\phi$ 定义的编码器上得到的表示。这样的做法有**两个好处**：
1. 使用编码器得到的不同特征有助于我们提取不同视角和模态的数据特征，来实现更好的建模
2. 数据编码后的结果处于一个更低维度的表示空间中，我们可以通过这种方式实现数据的降维
同时，信息最大化的$\mathcal{I}$ 往往通过**对比学习**来实现，对比学习是一种无监督的学习方式，通过构造正样本对和负样本对，并让他们进行对比来学习高质量的数据表示。由于直接计算互信息比较困难，因此现在已有的研究往往通过最大化InfoNCE loss来实现。

InfoMax-GAN模型的总体架构如下图所示：
![](resources/Pasted%20image%2020230208160827.png)
和原生GAN相比，InfoMax-GAN主要多了一个对比的过程，这个对比的过程大致是这样的：将一张数据集中的图片或者由噪声生成的图片输入判别器，判别器中有一个ResNet作为backbone对输入图像进行编码，我们取ResNet最后一次的输出结果，经过一个线性投影层$f$ 得到全局的表示$E$， 同时将原本的feature map作为局部特征表示。局部特征和全局特征分别经过一次投影之后再进行InfoNCE loss的计算来完成in-batch的对比(就是一个batch的数据互相进行对比)，这个过程可以表示为：

$$
\begin{aligned}
\mathcal{L}_{n c e}(X) & =-\mathbb{E}_{x \in X} \mathbb{E}_{i \in \mathcal{A}}\left[\log p\left(C_\psi^{(i)}(x), E_\psi(x) \mid X\right)\right] \\
& =-\mathbb{E}_{x \in X} \mathbb{E}_{i \in \mathcal{A}}[\Delta] \\
\Delta & =\log \frac{\exp \left(g_{\theta, \omega}\left(C_\psi^{(i)}(x), E_\psi(x)\right)\right)}{\sum_{\left(x^{\prime}, i\right) \in X \times \mathcal{A}} \exp \left(g_{\theta, \omega}\left(C_\psi^{(i)}\left(x^{\prime}\right), E_\psi(x)\right)\right)}
\end{aligned}
$$

其中$g_{\theta, \omega}$ 是一个打分函数，将输入的样本映射成一个标量分数。它的计算过程如下：

$$
g_{\theta, \omega}\left(C_\psi^{(i)}(x), E_\psi(x)\right)=\phi_\theta\left(C_\psi^{(i)}(x)\right)^T \phi_\omega\left(E_\psi(x)\right)
$$

- 注意，这里将局部特征分成了若干份，每一份都和全局特征作为一对正样本参与到对比中。
- 这是一个辅助loss，论文中添加了一个系数之后将其添加到了训练生成器和判别器的loss中
- 虽然看起来idea非常简单，但是论文花了好几大段来论述为什么对比学习可以：
	- Mitigating Catastrophic Forgetting
	- Mitigating Mode Collapse

## 2. XMC-GAN
> 原论文[Cross-Modal Contrastive Learning for Text-to-Image Generation](https://arxiv.org/abs/2101.04702) 发表于CVPR2021

这篇文章针对图像到文本的生成任务(实际上就是一个conditional GAN)设计了很多对比学习的loss，汇总成了他们的模型XMC-GAN，模型的总体架构如下：
![](resources/Pasted%20image%2020230208182500.png)
可以看到整个模型总体上还是分为生成器和判别器两个部分，不过生成器的self-modulation设计我们不需要关系，我们主要关系判别器中对比学习的设计。在论文中，作者主要设计了三个对比学习的模块：
- Image-text的对比，对于一个句子-图像对(可以是真实数据也可以是生成的)，用编码器分别提取他们的特征，然后作为一对正样本计算cosine相似度，然后进行in-batch的对比
- Real image-fake image的对比，对于一段文本，将其对应的真实图片和生成器生成的图片作为一对正样本，并进行in-batch的对比
- Word-region的对比，提取句子中的每个单词和图像中每个region的表示，然后计算每个单词对每个region的注意力权重，得到每个单词对整张图像的注意力加权表示，然后聚合得到整个句子对于整个图像的分数，并进行in-batch的对比，这个过程如下：

$$
\alpha_{i, j}=\frac{\exp \left(\rho_1 \cos \left(f_{\text {word }}\left(w_i\right), f_{\text {region }}\left(r_j\right)\right)\right)}{\sum_{h=1}^R \exp \left(\rho_1 \cos \left(f_{\text {word }}\left(w_i\right), f_{\text {region }}\left(r_h\right)\right)\right)}
$$

$$
\mathcal{S}_{\text {word }}(x, s)=\log \left(\sum_{h=1}^T \exp \left(\rho_2 \cos \left(f_{\text {word }}\left(w_h\right), c_h\right)\right)\right)^{\frac{1}{\rho_2}} / \tau
$$

$$
\mathcal{L}_{\text {word }}\left(x_i, s_i\right)=-\log \frac{\exp \left(\mathcal{S}_{\text {word }}\left(x_i, s_i\right)\right)}{\sum_{j=1}^M \exp \left(\mathcal{S}_{\text {word }}\left(x_i, s_j\right)\right)}
$$

对本论文的总结：
- 多模态任务中，不同模态之间可以设计一个对比loss，同一模态的real/fake数据也可以进行对比，同类型的对比，可以设计不同粒度的loss(比如这篇文章有一次粗粒度的对比，也有一次使用注意力之后的细粒度对比)

## 3. DualContrastiveLoss
> 原论文：[Dual Contrastive Loss and Attention for GANs](https://ieeexplore.ieee.org/document/9710622) 发表于ICCV 2021

感觉是一篇莫名其妙的水文，不过还是可以看看。
![](resources/Pasted%20image%2020230208224607.png)
这篇文章中对比学习的主要设计是在判别器中加对比学习的模块，和前面几篇文章将其作为辅助loss不同，该论文提出的方法是直接把这种real/fake的对比作为主loss，具体的过程分为两个case，如下所示：

$$
\begin{array}{l}
L_{\text {real }}^{\text {contr }}(G, D)=\underset{\mathbf{x} \sim p(\mathbf{x})}{\mathbb{E}}\left[\log \frac{e^{D(\mathbf{x})}}{e^{D(\mathbf{x})}+\sum_{\mathbf{z} \sim \mathcal{N}\left(\mathbf{0}, \mathbf{I}_d\right)} e^{D(G(\mathbf{z}))}}\right] \\
\quad=-\underset{\mathbf{x} \sim p(\mathbf{x})}{\mathbb{E}}\left[\log \left(1+\sum_{\mathbf{z} \sim \mathcal{N}\left(\mathbf{0}, \mathbf{I}_d\right)} e^{D(G(\mathbf{z}))-D(\mathbf{x})}\right)\right]
\end{array}
$$

$$
\begin{array}{l}
L_{\text {fake }}^{\text {contr }}(G, D)=\underset{\mathbf{z} \sim \mathcal{N}\left(\mathbf{0}, \mathbf{I}_d\right)}{\mathbb{E}}\left[\log \frac{e^{-D(G(\mathbf{z}))}}{e^{-D(G(\mathbf{z}))}+\sum_{\mathbf{x} \sim p(\mathbf{x})} e^{-D(\mathbf{x})}}\right] \\
=-\underset{\mathbf{z} \sim \mathcal{N}\left(\mathbf{0}, \mathbf{I}_d\right)}{\mathbb{E}}\left[\log \left(1+\sum_{\mathbf{x} \sim p(\mathbf{x})} e^{D(G(\mathbf{z}))-D(\mathbf{x})}\right)\right]
\end{array}
$$

整个GAN模型的训练目标就变成了：

$$
\min _G \max _D L_{\text {real }}^{\text {contr }}(G, D)+L_{\text {fake }}^{\text {contr }}(G, D)
$$

总之非常神奇，这样的方法居然是有效的。

