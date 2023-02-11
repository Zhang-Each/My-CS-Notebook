# Causality04-Intervention&Backdoor Adjustment
上一节中，我们使用因果图，对因果模型给出了直观的解释，但是因果图模型本身没有解释如何识别出因果量并对其进行定量的分析，这一节的任务就是探讨这个问题。

## 1. do-operator
为了对因果量进行定量的分析，我们首先要引入一种操作叫做intervention，也就是干预，这个概念和我们在概率论中学到的conditioning概念有所不同，以$T=t$为条件，只是意味着我们将注意力限制在接受治疗t的受试者子集上；而干预措施是对整个受试者群体进行干预，让每个人都接受t治疗。二者的区别可以用下面这张图来表示：
![](resources/Pasted%20image%2020230209170412.png)

我们用do算子来表示干预的过程，$do(T=t)$表示进行$T=t$的干预，这个表示方法是在因果图模型中常用的，而在潜在结果框架中，我们也有类似的用法。比如，我们可以这样写：

$$
P(Y(t)=y) \triangleq P(Y=y \mid d o(T=t)) \triangleq P(y \mid d o(t))
$$

这里面的$P(Y|do(T=t))$被称为干预分布(interventional distributions)，是我们后面重点研究的对象。干预分布和观测到的分布$P(Y)$有所区别，观测到的分布中不包含do算子，如果我们可以把一个包含do算子的表达式Q(对应干预分布)还原成一个没有do算子的表达式(对应观测分布)，那么我们称Q为可识别的(identifiable)
- 带有do的表达式与没有do的表达式有着本质上的区别，尽管在写的时候它看起来和条件概率的用法一样，但实际上他们表达的意思不同。包含do的概率表达式在估计的时候进行的是causal estimand，条件概率表达式在估计的时候是statistical estimand
- 如果一个表达式中出现了do算子，那么这个表达式中除了被干预的量以外，其他所有变量都处于"干预后的世界中"，比如在$P(Y|do(t),Z=z)$ 中，$Z=z$代表的是对T进行干预之后满足$Z=z$的那部分数据。

## 2. The Main Assumption: Modularity

对于一个节点来说，因果机制(causal mechanism)指的是它的parents以及对应的边(也就是cause)，记做$P(x_i|pa_i)$，比如下面这个例子中，被圈出来的部分就是节点$X_i$的因果机制：
![](resources/Pasted%20image%2020230210104042.png)


为什么要提出因果机制的概念呢？这是为了进一步提出我们的假设。为了得到更多可识别的因果结果，我们将作出的主要假设是，**干预是局部的**。也就是说，我们假设，对一个变量$X_i$的干预只改变$X_i$对应的那些因果机制，而不改变产生任何其他变量的因果机制。从这个假设来看，因果机制是模块化的(模块性也被称为独立机制、自主性和不变性)，这个假设的具体表述为：
> 如果我们对概率图中的一些节点$S \subseteq[n]$进行干预，将这些节点设定为了常量，那么对于所有的节点i，我们有：
> 1. 如果$i\not\in S$，那么$P(x_i|pa_i)$保持不变
> 2. 如果$i\in S$，那么，假设干预的值设定为$X_i=x_i$，那么$P(x_i|pa_i)=1$，否则$P(x_i|pa_i)=0$

乍一看感觉很抽象，其实这样的假设还是贴合“干预操作”的本意的，因为干预操作需要改变原本的概率分布，而模块化假设可以帮助我们更容易地计算概率分布。
模块化假设可以让我们用一个因果图来编码多种不同的干预，比如$P(Y),P(Y|do(T=t)), P(Y|do(T=t')), P(Y|do(T_2=t_2))$是四个完全不同的概率分布，但是它们都可以在一个因果图中表示(只要我们指定后续干预的变量是谁)，干预分布的因果图**由观察到的联合分布的图是去掉了所有与干预节点的边**之后得到，这是因为被干预的节点的概率已经被设置成了1，所以所有指向当前节点的边都已经不需要了。另一个角度来看，被干预的节点已经被设定为了一个常数，也就不再依赖于原本那些parents了。下图就是一个例子：
![](resources/Pasted%20image%2020230210145335.png)

## 3.  Truncated Factorization
我们之前说过贝叶斯网络的分解方式：

$$
P\left(x_1, \ldots, x_n\right)=\prod_i P\left(x_i \mid \mathrm{pa}_i\right)
$$

也就是把所有概率的联合分布简化成一系列条件概率。但是当我们对一些节点进行干预的时候，其中的一些条件概率分布$P\left(x_i \mid \mathrm{pa}_i\right)$就会发生改变，这时候整个式子也会发生改变，我们有：

$$
P\left(x_1, \ldots, x_n \mid d o(S=s)\right)=\prod_{i \notin S} P\left(x_i \mid \mathrm{pa}_i\right)
$$

这个公式被称为阻塞分解Truncated Factorization，它意在表明，一些节点被干预的时候如何计算总体的概率分布。
- 要注意的是，这是和干预一致时的情况，否则整体的概率分布就是0
下面我们通过一个例子来感受一下如何使用阻塞分解公式。我们以下面这个因果图为例，图中有X, Y, T三个变量，其中X是confounder，会同时影响T和Y，现在我们要来估计T对Y的因果效应。
![](resources/Pasted%20image%2020230210163558.png)


首先，三个变量的联合概率分布是：

$$
P(y, t, x)=P(x) P(t \mid x) P(y \mid t, x)
$$

当我们对treatment T进行干预的时候，我们可以得到：

$$
P(y, x \mid d o(t))=P(x) P(y \mid t, x)
$$

我们对x进行边缘化(marginalize)，可以得到：

$$
P(y\mid d o(t))=\sum_{x} P(y, x \mid d o(t))=\sum_{x} P(x) P(y \mid t, x)
$$

这是一个非常好的例子来帮助我们认识关联$P(y\mid t)$和因果$P(y\mid d o(t))$的区别，如果上面这个式子中的$P(x)$换成$P(x\mid t)$，那么我们就可以得到：

$$
\sum_{x} P(x\mid t) P(y \mid t, x)=\sum_{x}P(y,x\mid t)=P(y\mid t)
$$

这表明，关联$P(y\mid t)$和因果$P(y\mid d o(t))$的区别**实际上是**$P(x), P(x\mid t)$**的区别**，如果我们考虑的是treatment为t的时候x的分布，那么计算得到的结果就是关联，如果考虑了全局的x的概率分布，那么计算得到的结果就是因果。
另一方面，ATE的计算可以转化成：

$$
\mathbb{E}[Y(1)-Y(0)]=\sum_y y P(y \mid d o(T=1))-\sum_y y P(y \mid d o(T=0))
$$

我们把上面的$P(y\mid do(t))$计算方法缝进这个表达式里，就可以计算出一个fully identified ATE，这样一来，我们**只需要观测到的数据分布就可以计算因果效应**，这就是前面所说的identification

## 4. Backdoor Adjustment
根据前一节内容，我们知道在上面这张因果图中，T和Y因果关系会沿着有向边流动，而非因果的关联会沿着T到Y的任何未阻塞路径(并且满足路径中存在一个conditioned non-collider，或者一个conditioned collider)流动，这些未阻塞的非有向路径被称为**后门路径(Backdoor Path)**，因为这些路径打开了一条通往T的“后门”，如果我们能够阻断这些路径，我们就能估计T对Y的因果效应。
- 我的理解是，因为要估计T对Y的因果效应，就必须固定$T=t$，而由于后门路径会指向T，所以为了保证T是固定的，必须要阻断这条后门路径。
对于什么样的变量可以算是“后门”，我们有一个具体的判断规则，这被称为**后门标准(Backdoor Criterion)**，具体如下：
> 一系列变量集合W如果满足：(1).  W阻塞了所有T和Y之间的后门路径，(2). W不包含T的任何后代节点，那么就说W相对于T和Y满足后门标准。
- 事实上这样的W也一定是T和Y的d-分割
这样一来，W就被称为充分调整集，比如在上面那个TXY的例子中，X就是这个变量集合W，我们结合模块性假设以及基本的概率论工具可以推出：

$$
\begin{aligned}
P(y \mid d o(t))&=\sum_w P(y \mid d o(t), w) P(w \mid d o(t))\\
&=\sum_w P(y \mid t, w) P(w \mid d o(t))\\
&=\sum_w P(y \mid t, w) P(w)
\end{aligned}
$$

这个推导过程中，第一步是基于全概率公式，第二步是基于模块化假设，第三步则是基于后门准则(因为W不包含X的后代，所以X怎么do都和W无关)，这样一来，我们就得到了后门调整公式：

> 在满足模块性假设的前提下，如果W相对于T和Y满足后门准则，那么T和Y之间的因果效应可以被识别为：

$$
P(y \mid d o(t))=\sum_w P(y \mid t, w) P(w)
$$

有了后门调整公式，我们就可以把因果效应的计算转化为统计量(观测到的数据的概率分布)。
我们在回忆一下之前提到的潜在结果公式：

$$
\mathbb{E}[Y(1)-Y(0)]=\mathbb{E}_W[\mathbb{E}[Y \mid T=1, W]-\mathbb{E}[Y \mid T=0, W]]
$$

可以发现它的形式和后门调整有些相似，我们可以对$P(y\mid do(t))$求个期望，可以得到下面的推导：

$$
\begin{aligned}
\mathbb{E}[Y \mid d o(t)]&=\sum_w \mathbb{E}[Y \mid t, w] P(w)\\
&=\mathbb{E}_{W}\mathbb{E}[Y \mid t, w]
\end{aligned}
$$

这样一来，我们有：

$$
\mathbb{E}[Y \mid do(T=1)]-\mathbb{E}[Y \mid do(T=0)]=\mathbb{E}_{W}[\mathbb{E}[Y \mid T=1, w]-\mathbb{E}[Y \mid T=0, w]]
$$

而事实上，$\mathbb{E}[Y \mid do(T=t)]=\mathbb{E}[Y(t)]$，所以后门调整公式和因果效应的估计是相联系的，因此我们可以利用后门调整公式来估计因果效应，同时使用图模型，找到合适的混淆量W