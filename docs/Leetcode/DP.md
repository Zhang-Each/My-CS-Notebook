# 动态规划

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