# 位运算和逻辑操作(与/或/异或)

## 6369. 最大或值
> 给你一个下标从 0 开始长度为 n 的整数数组 nums 和一个整数 k 。每一次操作中，你可以选择一个数并将它乘 2 。
> 你最多可以进行 k 次操作，请你返回 nums[0] | nums[1] | ... | nums[n - 1] 的最大值。
> a | b 表示两个整数 a 和 b 的 按位或 运算。

这道题的关键在于发现把k次乘2全交给一个数，最终的结果可能会最好，因为一堆数字进行按位或运算只会不断变大，而要让最终的结果尽可能大，我们应该需要让nums中数字的位数尽可能多，这个时候把k次乘2全交给一个数字，显然可以获得尽可能大的结果，同时我们可以用前缀和来优化一下时间复杂度，最终的代码如下：

```python
class Solution:
    def maximumOr(self, nums: List[int], k: int) -> int:
        # 要让答案最大，首先应当最大化答案的二进制的长度。
        # 把k分配给多个数，不如只分配给一个数，这样更有可能得到更大的答案
        # 所以可以用前缀和+枚举的方式找出最大值
        n = len(nums)
        prefix = [0 for i in range(n + 1)]
        postfix = [0 for i in range(n + 1)]
        for i in range(n):
            prefix[i + 1] = prefix[i] | nums[i]
        for i in range(n - 1, -1, -1):
            postfix[i] = postfix[i + 1] | nums[i]
        result = 0
        for i in range(n):
            temp = prefix[i] | (nums[i] << k) | postfix[i + 1]
            result = max(result, temp)
        return result
        
```


## 6455. 使所有字符相等的最小成本
> 给你一个下标从 0 开始、长度为 n 的二进制字符串 s ，你可以对其执行两种操作：选中一个下标 i 并且反转从下标 0 到下标 i（包括下标 0 和下标 i ）的所有字符，成本为 i + 1 。选中一个下标 i 并且反转从下标 i 到下标 n - 1（包括下标 i 和下标 n - 1 ）的所有字符，成本为 n - i 。
> 返回使字符串内所有字符 相等 需要的 最小成本 。
> 反转 字符意味着：如果原来的值是 '0' ，则反转后值变为 '1' ，反之亦然。

让所有字符都相等，可以全是0或者可以全是1，根据题目的意思可以发现，如果从第i位到第j位的字符都是相同的，并且我们要对其进行反转，那么我们进行两次操作就可以了，首先反转0-j，再反转0
-i，或者从相反的方向做一遍。只需要统计一下这样的操作需要进行多少次，然后从两个方向中选出代价比较小的那一个，再求个和就可以了。具体的代码如下：

```python
class Solution:
    def minimumCost(self, s: str) -> int:
        n = len(s)
        target = ["0" * n, "1" * n]
        result = []
        for t in target:
            res = 0
            i = 0
            while i < n:
                start = i
                while start < n and s[start] == t[start]:
                    start += 1
                end = start
                while end < n and s[end] != t[end]:
                    end += 1
                i, end = end, end - 1
                # 从start-end一起换掉
                temp1 = end + 1 + start - 1 + 1
                temp2 = (n - (end + 1)) + (n - start)
                res += min(temp1, temp2)        
            result.append(res)
        return min(result)
```