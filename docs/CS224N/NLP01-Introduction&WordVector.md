NLP01-Introduction
============

自然语言处理简介
----------------

自然语言处理是对人类语言的分析和处理，人类的语言(也就是自然语言)是一种专门为传达意思而构建的系统，并不是任何物理设备生成的，因此自然语言和图像或者其他一些机器学习任务有很大的不同。不管是什么自然语言，总是由一系列单词组成的，而这些单词中的大部分仅仅代表的是一种语言以外的实体，也就是说单词是一种能指(signifier，即单词本身)到所指(signified，单词所代表的含义)的映射。

自然语言处理建模的对象可以包括单词，句子，文章，文档等一系列包含自然语言的对象。

### 自然语言处理的任务

自然语言处理中有很多种不能难度等级的任务，但总的来说自然语言处理的目标是让计算机可以"理解"人类的语言，这些任务可以根据难度分成这样几个等级：

-   Easy：拼写检查，关键词检索，找同义词

-   Medium：解析复杂文档，包括web文档和其他结构化的文档

-   Hard：机器翻译，语义分析，引用推断(Coreference)和自动问答

后面的内容将主要围绕基于深度学习方法来完成自然语言处理的各项任务。

### 如何表示单词

所有的自然语言都是由若干的单词或者说词汇组成的，NLP的建模最重要的一个任务就是对单词进行建模，采用一定的方式来表示各种单词，因为后面介绍的大部分NLP任务都将单词看成一种atomic
symbols，也就是原子符号，即不可拆分的最基本单位，我们的首要任务就是完成对单词的建模。

我们可以使用向量来表示一个单词，将单词的特征编码到向量的一系列维度中，这也就是词向量(Word Vector)

词向量也就是用向量来表示一个单词，但是语言的单词数量可能是非常庞大的，比如英语就有各类单词词组约1300万个，我们需要将这些单词全部编码到一个N维度的向量中去，向量的每个维度可以编码一些语义或者单词的特征。词向量也可以叫做词嵌入Word Embedding​

one-hot词向量
-----------

一种非常不负责任的编码方式就是one-hot向量，这种方法根据当前样本数据的词汇表的大小$|V|$，用一系列维度为$|V|$的0-1向量来代表单词，词汇表中出现的每个单词$m$有一个对应的维度$v_m$，每个单词对应的词向量中，该维度的值是1，其他的维度都是0，这种方式非常简单粗暴，但是问题也很明显，这样的编码是非常**稀疏**的，词向量中的大部分内容都是无效信息0，并且词向量的规模也非常大，是对计算资源的严重浪费。



基于奇异值分解SVD的词向量
-------------------------

### 奇异值分解SVD

根据我们仅存的一点线性代数的知识，我们知道矩阵可以分解成一系列特征向量和特征值，但是除此之外矩阵还可以进行奇异值分解(Singular Value Decomposition, SVD)是将矩阵分解成一系列奇异向量和奇异值

这种方法可以使我们得到一些和特征分解类似的信息，**但是相比于特征分解，奇异分解适用范围更广，所有的实矩阵都有一个奇异值分解但不一定有特征分解(特征分解必须要是方阵)**。
在特征分解中我们可以求出一系列特征向量使其构成一个矩阵$V$和一系列特征值构成对角矩阵$\mathrm{diag}(\lambda)$，这样一来一个矩阵就可以分解成：
$$
A=V\mathrm{diag}(\lambda) V^{-1}
$$
而在奇异值分解中我们可以类似地将矩阵分解成三个矩阵的乘积：
$$
A=UDV^{-1}
$$
这里我们可以假设A是一个$m\times n$维的矩阵那么U是一个$m\times m$的矩阵，D是一个$m\times n$的矩阵，V是一个$n\times n$的矩阵并且U和V都是正交矩阵，而D是一个对角矩阵。

对角矩阵D的对角线上的元素就是矩阵A的奇异值，U和V分别被称为左右奇异向量，事实上这种分解方式可以理解为：D就是$AA^T$特征值的平方根，而U和V分别是$AA^T$和$A^TA$的特征向量，实际上就是我们将任意一个实矩阵通过一定的变换变成了一个方阵，然后对方阵进行奇异值分解反过来表示原本矩阵的一些特征。

因此我们可以适用奇异值分解的办法来提取一个单词的嵌入向量，但是我们首先需要将数据集中海量的单词汇总成一个矩阵X并对该矩阵进行奇异值分解，然后可以将分解得到的U作为所有单词的嵌入向量，而生成矩阵X的方法有多种选择。

### 单词文档矩阵Word-Document Matrix

我们可以假设相关的单词总会在同一篇文档中出现，利用这一假设来建立一个单词文档矩阵，其中$X_{ij}=1$表示单词$w_i$出现在了文档$d_j$中，否则就是0，这样一来矩阵的规模就是$|V|\times M$，规模是非常庞大的。

### 基于窗口的共生矩阵Co-occurrence Matrix

我们可以使用一个固定大小的滑动窗口来截取文档中的单词组合，然后对每一次采样得到的单词进行计数，如果单词a和单词b在一次采样结果中同时出现，就在矩阵X上给它们对应的位置的值+1(相同的单词不考虑)，这样一来可以得到一个大小为$|V|\times |V|$的矩阵并且U和V都是正交矩阵，而D是一个对角矩阵。

### SVD的使用

在获得的矩阵X上使用SVD的时候，最后得到的每个单词的嵌入向量是$|V|$维的，我们可以进行截取，只保留k维：

$$
\frac{\sum_{i=1}^k\sigma_i}{\sum_{i=1}^{|V|}\sigma_i}
$$

然后用截取得到的k维向量作为每个单词的嵌入向量。

### SVD方法的缺陷与解决

SVD方法还是存在一定的缺陷的，不管用什么方式生成矩阵X，都会面临这样几个问题：

-   计算量较大，对于$m\times n$的矩阵，SVD的时间复杂度是$O(mn^2)$，因此维数高了以后计算量会暴增

-   生成的矩阵要插入新单词或者新文档的内容时比较麻烦，矩阵的规模很容易变化

-   生成的矩阵往往比较稀疏，因为大部分单词和单词或者单词和文档之间可能没什么关系

面对这些问题，可以采取的解决措施有：

-   不考虑一些功能性的单词比如a，an，the，it等等

-   使用一个倾斜的窗口，也就是在生成共生矩阵的时候考虑单词相距的距离


