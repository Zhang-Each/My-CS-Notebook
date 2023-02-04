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


