# 动态规划

## 0005. 最长回文子串
> 给你一个字符串 s，找到 s 中最长的回文子串。如果字符串的反序与原始字符串相同，则该字符串称为回文字符串。

经典的动态规划问题，用一个数组`dp[i][j]`表示s从i到j这一段是不是回文字符串，dp的情况可以分成下面几种：
- 如果`i == j` 那么很明显是的
- 如果`i + 1 == j` 那么就看`s[i + 1] == s[j]`是否成立
- 其他情况，要先判断`s[i + 1] == s[j - 1]`是否成立，然后再根据`dp[i + 1][j - 1]`是不是1来决定`dp[i][j]`的结果
同时，因为遍历过程中，需要知道i+1的情况，所以第一层关于i的循环要倒着进行，保证`dp[i + 1][j - 1]`是一个有效值。具体的代码如下：

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[0 for i in range(n)] for j in range(n)]
        maxl = 1
        res = s[0]
        # 经典dp，经典中的经典
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1
            for j in range(i + 1, n):
                if j == i + 1:
                    dp[i][j] = 1 if (s[i] == s[j]) else 0
                else:
                    if s[i] == s[j]:
                        dp[i][j] = dp[i + 1][j - 1]
                    else:
                        dp[i][j] = 0
                if dp[i][j] and j - i + 1 > maxl:
                    maxl = j - i + 1
                    res = s[i: j + 1]
        return res

```

## 1653. 使字符串平衡的最少删除次数
> 给你一个字符串 s ，它仅包含字符 'a' 和 'b'​​​​ 。你可以删除 s 中任意数目的字符，使得 s 平衡 。当不存在下标对 (i,j) 满足 i < j ，且 s[i] = 'b' 的同时 s[j]= 'a' ，此时认为 s 是 平衡 的。
> 请你返回使 s 平衡 的 最少 删除次数。

这道题目的意思非常明确，就是要把字符串s处理成前面全是a后面全是b的形式(当然a和b可以没有)
我们可以将这个问题转化成一个DP问题，用dp表示字符串s的最少删除次数，如果我们在s尾部新增一个字符，那么dp的更新可以分成两种情况讨论：
- 如果新增了一个a，我们可以把这个a删除，或者把前面的b全部删除，我们需要记录前面b的个数
- 如果新增了一个b，因为前面的字符串已经平衡了，所以可以先记录b的数量，不需要进行删除操作
最终的代码如下：

```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        # 所有的a必须出现在所有的b前面，当然a也可以没有
        count = 0
        dp = 0
        for i in s:
            # 简单动态规划，如果最后是a，要不就删除，要不就把前面的b全部删除
            if i == 'a':
                dp = min(dp + 1, count)
            else:
                count += 1
        return dp
```



## 6310. 获得分数的方法数
> 考试中有 n 种类型的题目。给你一个整数 target 和一个下标从 0 开始的二维整数数组 types ，其中 types[i] = [counti, marksi] 表示第 i 种类型的题目有 counti 道，每道题目对应 marksi 分。
> 返回你在考试中恰好得到 target 分的方法数。由于答案可能很大，结果需要对 109 +7 取余。

这道题是一道很经典的dp计数的题目，我们可以开一个长度为target+1的数组dp，dp[i]代表了分数恰好为i的时候的方案总数，并遍历types数组，对可以获得的分数进行dp，具体的代码如下：

```python
class Solution:
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        dp = [0 for i in range(target + 1)]
        mod = 10 ** 9 + 7
        dp[0] = 1
        # 直接dp居然真的可以过，惊了
        for tp in types:
            c, m = tp
            for i in range(target, -1, -1):
                for j in range(1, min(c, i // m) + 1):
                    dp[i] = (dp[i] + dp[i - j * m]) % mod
        return dp[-1]
```