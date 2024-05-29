
# 1. 深度学习基础

逻辑回归

激活函数

标准化

Loss函数


# 2. NLP基础

词向量

RNN和LSTM

注意力机制


# 3. Transformer与BERT

Transformer的架构

Self-attention的实现

Position encoding的作用

Transformer的Encoder和Decoder的区别

BERT的预训练方式

## Pre-Norm和Post-Norm的区别
两者都是LLM常见的Normalization的操作，区别在于Layer Normalization层的位置不同，Pre-Norm是在数据进入残差链接之间就先进行LN，而Post-Norm是在计算完残差之后才计算LN的结果，一般来说，Post-Norm对参数的正则化的效果更强，进而模型的收敛性较好，而Pre-Norm有一部分参数直接加在了后面，没有对这部分参数进行正则化，可以在反向传播时防止梯度爆炸或者梯度消失，使得模型更容易训练，大模型的训练难度大，因而使用Pre-Norm较多。同一设置之下，Pre Norm结构往往更容易训练，但最终效果通常不如Post Norm
![](resources/Pasted%20image%2020240308133636.png)
- Llama中用的是pre-norm，方便模型的训练


## RMS-Norm
RMS Norm全称是**Root Mean Square Layer Normalization**，与RMS Norm是基于LN的一种变体，主要是去掉了减去均值的部分，计算公式如下：
![](resources/Pasted%20image%2020240308134016.png)
主要的改进就是去掉了LN层中跟均值有关的统计量的计算，加快了模型训练时候的效率，可以看作LayerNorm在均值为0时的一个特例。原论文通过实验证明，re-center操作不重要。
- Llama模型中用的就是RMS的归一化操作







# 4. 大语言模型

BERT和GPT的区别

## MHA/MQA/GQA

MHA（Multi-head Attention）是标准的多头注意力机制，h个Query、Key 和 Value 矩阵。
MQA（Multi-Query Attention，Fast Transformer Decoding: One Write-Head is All You Need）是多查询注意力的一种变体，也是用于自回归解码的一种注意力机制。与MHA不同的是，MQA 让所有的头之间共享同一份 Key 和 Value 矩阵，每个头只单独保留了一份 Query 参数，从而大大减少 Key 和 Value 矩阵的参数量。
GQA（Grouped-Query Attention，GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints）是分组查询注意力，GQA将查询头分成G组，每个组共享一个Key 和 Value 矩阵。GQA-G是指具有G组的grouped-query attention。GQA-1具有单个组，因此具有单个Key 和 Value，等效于MQA。而GQA-H具有与头数相等的组，等效于MHA。

## ZeRO的三个阶段

> 部分内容来源于知乎https://zhuanlan.zhihu.com/p/394064174

模型在训练过程中 Model States 是由什么组成的：
1. Optimizer States: Optimizer States 是 Optimizer 在进行梯度更新时所需要用到的数据，例如 Adam 中的Momentum以及使用混合精度训练时的Float32 Master Parameters。 
2. Gradient： 在反向传播后所产生的梯度信息，其决定了参数的更新方向。 
3. Model Parameter: 模型参数，也就是我们在整个过程中通过数据“学习”的信息。
当通过数据并行在训练模型的时候，这些重复的Model States会在N个GPU上复制N份。ZeRO 则在数据并行的基础上，引入了对冗余Model States的优化。使用 ZeRO 后，各个进程之后只保存完整状态的1/GPUs，互不重叠，不再存在冗余。在本文中，我们就以这个 7.5B 参数量的模型为例，量化各个级别的 ZeRO 对于内存的优化表现。

ZeRO 有三个不同级别，分别对应对 Model States 不同程度的分割 (Paritition)： 
- ZeRO-1：分割Optimizer States；在进行梯度更新时，会使用参数与Optimizer States计算新的参数。而在正向或反向传播中，Optimizer States并不会参与其中的计算。 因此，我们完全可以让每个进程只持有一小段Optimizer States，利用这一小段Optimizer States更新完与之对应的一小段参数后，再把各个小段拼起来合为完整的模型参数。
- ZeRO-2：分割Optimizer States与Gradients；进一步对梯度进行切片处理
- ZeRO-3：分割Optimizer States、Gradients与Parameters，在ZeRO-2的基础上将模型的参数也进行切片，通过精细化的通讯，在只存储一份完整的Model States的情况下，所有进程共协作完成训练





## 什么是MoE(Mix-of-Experts)?

> 主要内容来源于huggingface上的博客 https://huggingface.co/blog/zh/moe

混合专家模型（Mixture of Experts：MoE）由多个专业化的子模型（即“专家”）组合而成，每一个“专家”都在其擅长的领域内做出贡献。而决定哪个“专家”参与解答特定问题的，是一个称为“门控网络”的机制。这种思想其实来源于早期的集成学习。
LLM领域由于Mixtral 8x7B的惊人性能，导致现在MoE相关的技术备受关注，具体来说，MoE的LLM和稠密模型相比有以下几个特点：
- 与稠密模型相比， 预训练速度更快
- 与具有相同参数数量的模型相比，具有更快的 推理速度
- 需要更多的显存，因为所有专家系统都需要加载到内存中
模型规模是提升模型性能的关键因素之一。在有限的计算资源预算下，用更少的训练步数训练一个更大的模型，往往比用更多的步数训练一个较小的模型效果更佳。混合专家模型 (MoE) 的一个显著优势是它们能够在远少于稠密模型所需的计算资源下进行有效的预训练。这意味着在相同的计算预算条件下，您可以显著扩大模型或数据集的规模。特别是在预训练阶段，与稠密模型相比，混合专家模型通常能够更快地达到相同的质量水平。

混合专家模型主要由两个关键部分组成:

- 稀疏 MoE 层: 这些层代替了传统 Transformer 模型中的**前馈网络 (FFN) 层**。MoE 层包含若干“专家”(例如 8 个)，每个专家本身是一个独立的神经网络。在实际应用中，这些专家通常是前馈网络 (FFN)，但它们也可以是更复杂的网络结构，甚至可以是 MoE 层本身，从而形成层级式的 MoE 结构。
- 门控网络或路由: 这个部分用于决定哪些令牌 (token) 被发送到哪个专家。例如，在下图中，“More”这个令牌可能被发送到第二个专家，而“Parameters”这个令牌被发送到第一个专家。有时，一个令牌甚至可以被发送到多个专家。令牌的路由方式是 MoE 使用中的一个关键点，因为路由器由学习的参数组成，并且与网络的其他部分一同进行预训练。

以 Mixtral 8x7B 这样的 MoE 为例，需要足够的 VRAM 来容纳一个 47B 参数的稠密模型。之所以是 47B 而不是 8 x 7B = 56B，是因为在 MoE 模型中，只有 FFN 层被视为独立的专家，而模型的其他参数是共享的。此外，假设每个令牌只使用两个专家，那么推理速度 (以 FLOPs 计算) 类似于使用 12B 模型 (而不是 14B 模型)，因为虽然它进行了 2x7B 的矩阵乘法计算，但某些层是共享的。
![](resources/Pasted%20image%2020240302235108.png)


门控网络在具体实现的时候可以通过添加一些自然噪声使得模型负载均衡，不至于使得所有内容都被发送给一个专家进行处理。