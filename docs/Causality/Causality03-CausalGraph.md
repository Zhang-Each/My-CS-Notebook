# Causality03-CausalGraph
前面我们实际上已经见到过了用概率图模型表示变量之间关系的例子，这是一种很直观的方法，在这一节，我们将重点介绍概率图模型的方法在因果推断中的应用。

## 1. Graph and Graphic Models

## 1.1 Graph
我们知道图(Graph)是由一系列节点和边组成的，图中的路径(path)是由一系列相邻的节点和边组成的序列。同时根据边是否有方向可以把图分为**有向图和无向图**两类。
- 有向图中的路径$X\rightarrow Y$ 表示X到Y有一条有向边，这个时候，X被称为ancestor，而Y被称为descendant，我们用$de(X)$表示X的descendant
- 有向图可以根据图中是否有环再分为两类，一类是有环图，一类是无环图，在因果推断中，我们主要研究的是有向无环图(directed acyclic graph, DAG)
概率图模型(probabilistic graphical model)就是通过图结构的形式来研究随机变量之间的关系，而因果图模型(causal graphical models)也是通过有向无环图的方式来建模变量之间的因果关系(概率图模型中的有向图模型叫做贝叶斯网络Bayesian networks)，有非常多的东西可以直接从概率图模型那边借鉴过来，区别在于，概率图模型是统计模型，而因果图模型是因果模型。

## 1.2 Bayesian Networks
对于一个有n个变量组成的贝叶斯网络，我们根据基本的概率论常识可以得到下面这个公式：

$$
P\left(x_1, x_2, \ldots, x_n\right)=P\left(x_1\right) \prod_i P\left(x_i \mid x_{i-1}, \ldots, x_1\right)
$$

这也就是建模n个变量总体概率分布情况的基本方法，对于这个公式，我们需要关注的就是如何计算$P(x_i \mid x_{i-1}, \ldots, x_1)$，假设$x_i$都是binary variable，那么我们建模这个计算过程，就需要$2^{n-1}$个参数，但是这样的建模方式会随着n的变大而产生指数级别的增长，这显然是不够scalable的，需要我们想办法解决。
一个很直观的方法就是将一些局部独立的变量看成一个整体来考虑，换句话说，就是考虑它们的joint distribution，比如下图的例子中，$X_4$只依赖于$X_3$，因此当我们有$P(X_4|X_3,X_2,X_1)=P(X_4|X_3)$，这样一来，需要考虑的参数量就变少了。
![](resources/Pasted%20image%2020230204183655.png)
>这实际上就是概率图模型中的Local Markov Assumption，这个假设是说， 给定X的父母节点，那么X和所有非后代节点都是独立的。

根据Local Markov Assumption，我们可以对上面这个例子的概率分布做如下化简：

$$
\begin{aligned}
P\left(x_1, x_2, x_3, x_4\right)&=P\left(x_1\right) P\left(x_2 \mid x_1\right) P\left(x_3 \mid x_2, x_1\right) P\left(x_4 \mid x_3, x_2, x_1\right)\\\
&=P\left(x_1\right) P\left(x_2 \mid x_1\right) P\left(x_3 \mid x_2, x_1\right) P\left(x_4 \mid x_3\right)
\end{aligned}
$$

也就是说，条件概率里的非后代节点都可以不用考虑，因此，我们可以推出贝叶斯网络的分解公式：

$$
P\left(x_1, \ldots, x_n\right)=\prod_i P\left(x_i \mid \mathrm{pa}_i\right)
$$

这里的pa就是表示$x_i$的父母节点，这个公式也被叫做chain rule for Bayesian networks
但是，贝叶斯网络分解没有说明相邻节点之间的相关性，因此，这本书上列出一个被称为Minimality Assumption的假设，它在Local Markov Assumption的基础上加了一条假设：
- DAG中的相邻节点都是相关的
这个假设被称为Minimality足见其重要性，这是因为，如果没有相邻节点不独立这条假设，我们在使用Local Markov Assumption的时候可能会引入额外的独立关系，比如考虑一个只包含两个节点X和Y的因果图，这个图里只有一条路径$X\rightarrow Y$，如果我们只使用Local Markov Assumption来进行分解，我们可能会得到$P(X,Y)=P(Y)P(X|Y)=P(X)P(Y)$，这是因为从X的角度来看，他没有父母节点，因此它对于Y是独立的，所以就会有这样的推导，我们在加上相邻节点相关的限制之后，这个推导就不成立了，我们只能推导出$P(X,Y)=P(X)P(Y|X)$
从贝叶斯网络中移除一些边就等价于额外添加了一些独立性，而Minimality Assumption的作用就在于，它要求贝叶斯网络中任何一条边都不能被删除，否则整个概率分布就会发生变化。

## 2. Causal Graph
### 2.1 Causal Edges Assumption
前面一节介绍的概率图是一种统计模型，这一节我们将讨论如何使用因果推断中的假设来增强概率图的建模，进而构造因果图(Causal Graph)来解决各种跟因果有关的问题。为了引入这些因果假设，我们需要先了解一下什么是因果。
> (Cause的定义)如果变量X的改变也会引起Y的改变，那么变量X被称为是Y的cause

我们在因果图中用一系列的节点来表示随机变量，用边来表示他们的关系，而在因果图中，我们做出了一个核心的假设：
> 严格的因果边假设：在有向图中，由父节点指向子节点的所有边都代表了父节点是子节点的一个cause

因果边假设实际上是由cause的定义以及概率图中的minmality assumption共同决定的。相比之下，非严格的因果边假设将允许一些父节点可以不是其子女的cause，它只是假设子女不是其父节点的原因。这样做可以减少我们作出的假设。
总之，1.2中提到的Local Markov Assumption和这一节提到的Causal Edges Assumption，将会成为我们研究因果图模型的基础，下面我们将更深入地研究概率图模型。

### 2.2 Graphical Building Blocks
DAG中有一些常见的基本构成模块，如下面两张图所示：

![](resources/Pasted%20image%2020230207132418.png)
![两个不相连的节点和两个相连节点](resources/Pasted%20image%2020230207131335.png)
书中提出了一个概念叫做flow of association，这个概念主要是用来表示两个节点是否独立(是否关联)，除此之外，我们会更进一步来研究两个节点是否条件独立。
#### 2.2.1 Two-node Graph
对于两个不相连的节点来说，很明显我们有：

$$
P\left(x_1, x_2\right)=P\left(x_1\right) P\left(x_2\right)
$$

也就是说两个节点是不相关的(互相独立的)，而对于两个相连的节点，他们显然是不独立的。

#### 2.2.2 Chain / Fork / Immorality
对于链结构和叉结构(如下图所示)，很显然，根据因果边假设，X1和X2是关联的，而X2和X3也是关联的。我们重点要研究的问题是，X1和X3之间是否具有关联性。
![](resources/Pasted%20image%2020230207134828.png)

![](resources/Pasted%20image%2020230207135030.png)
对于链结构来说，很明显X1和X3也是相关联的，因为X1导致X2，而X2导致X3，而对于叉结构来说，X1和X3也是相关联的，因为他们和同一个父节点X2相关联。但是当我们给定X2的时候，X1和X3就相互独立了，也就是说：

$$
X_1\perp\!\!\!\perp X_3 | X_2
$$

这其实非常容易证明，对于链结构，我们结合贝叶斯定理和X2给定这两个条件，可以作出如下推导证明：

$$
\begin{aligned}
P(x_1,x_3|x_2)&=\frac{P(x_1,x_2,x_3)}{P(x_2)}\\
&=\frac{P(x_1)P(x_2|x_1)P(x_3|x_2)}{P(x_2)}\\
&=P(x_1|x_2)P(x_3|x_2)
\end{aligned}
$$

这样一来，在给定$X_2=x_2$的条件下，$X_1, X_3$就是独立的。对于叉结构，证明就更容易了。
![](resources/Pasted%20image%2020230207202920.png)

对于上面这种immorality型结构，X1和X3明显是独立的，因为他们之间没有因果关系，但神奇的是，如果我们给定了X2(书上管X2叫做collider)，那么X1和X3就不独立了，这是因为他们共同决定了X2
- 值得注意的是，如果给定了collider的子节点，那么X1和X3也是不独立的
- 我们可以将上面说的这种情况理解为：原本X1和X3之间的cause path被X2阻塞(blocked)了，但是在给定X2之后，这条path就不阻塞(unblocked)了
- 事实上这可以通过一些简单的例子计算得到(比如定义X1和X3都是标准分布，然后计算他们的协方差)，不过这些内容就不在这里详细展开了

### 2.3 D-separation
#### 2.3.1 Blocked Path
上面我们提到了一个概念就是cause path的block(阻塞)和unblock(非阻塞)，在这里，我们给出blocked path的具体定义：
> 如果两个节点X和Y之间有一条路径，并且这个路径满足以下两个条件之一，那么这条路径就是一条blocked path：
> 1. 在这条路径上有一个链结构$\cdots \rightarrow W \rightarrow \cdots$或者一个叉结构$\cdots \leftarrow W \rightarrow \cdots$，并且W是conditioned的
> 2. 这条路径上有一个collider W，并且这个W不是conditioned的变量，W的所有后代节点也不是conditioned的变量

而一个unblocked path则是那些blocked path的补集，相关性会在unblocked path中传递，但是不会在blocked path中传递，这和前面的几个最简单的结构的例子是一致的。
### 2.3.2 d-separation
D-separation是因果图模型中一个非常重要的概念，它的定义如下：
> 对于两个节点(的集合)X和Y，如果存在一个节点集合Z，使得X和Y之间所有的路径都被Z所阻塞，那么Z就是X和Y的一个d-分割。类似地，如果X和Y之间存在非阻塞的路径，那么X和Y就是d-相连的。

d-分割是一个非常重要的概念，因为它可以表示两个(两组)变量之间的独立性关系，我们可以用$X\perp\!\!\!\perp _G Y|Z$ 来表示X和Y在图G上是一个关于Z的d-分割。如果在给定Z的条件下，X和Y在分布P中是条件独立的(是关于Z的一个d-分割)，那么就可以表示为$X\perp\!\!\!\perp _P Y|Z$
> 如果给定一个满足G上马尔可夫的联合概率分布P(即遵循局部马尔可夫假设)，那么如果X和Y在G中是关于Z的一个d-分割，则X和Y在P中也是条件独立的(或者说这个分布P是满足关于图G的全局马尔可夫性的)，即：


$$
X\perp\!\!\!\perp _G Y|Z\rightarrow X\perp\!\!\!\perp _P Y|Z
$$

这其实就是概率图模型中的**全局马尔可夫性**。从中我们可以看出全局马尔可夫性可以从局部马尔可夫性推导得出，这两个假设和贝叶斯网络分解其实都是等价的，是从不同角度对DAG的理解。我们将它们可以统称为马尔可夫假设。

### 2.4 Causal Association
在DAG中，我们将**沿着有向边流动的关联**称为因果关联(Causal Association)，而那些非因果的关联被称为混淆关联(Confounding Association)，下图就是一个简单的例子：
![](resources/Pasted%20image%2020230208111250.png)
不管是在概率图还是在因果图中，association都是沿着上面提到的基本结构进行流动的(当然要考虑中间是否有conditioned的节点)，因果图的特别之处在于，我们通过假设使得图中的边都代表了因果关系，同时，这样的因果关系和原本的关联关系也有所区别，如果A关联B，那么B也关联A，所以关联关系是一种对称的关系，而因果关系则是非对称的。我们可以用下面这张图来表示，随着假设的一步步引入，我们所研究的问题的变化，这也是对这几节所学内容的一次总结。
![](resources/Pasted%20image%2020230208111952.png)

