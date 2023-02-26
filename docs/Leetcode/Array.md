# 数组操作题

## 6368. 找出字符串的可整除数组
> 给你一个下标从 0 开始的字符串 word ，长度为 n ，由从 0 到 9 的数字组成。另给你一个正整数 m 。word 的 可整除数组 div  是一个长度为 n 的整数数组，并满足：如果 word[0,...,i] 所表示的 数值 能被 m 整除，div[i] = 1否则，div[i] = 0 返回 word 的可整除数组。

这道题的最大问题在于`word[0: i]` 可能非常大，导致直接去计算除以m的结果会很麻烦，我们可以用`word[0: i-1]`的余数乘以10再加上`word[i]`的值来计算第i次的余数，这样时间复杂度就降下来了，具体的代码如下：

```python
class Solution:
    def divisibilityArray(self, word: str, m: int) -> List[int]:
        n = len(word)
        div = [0 for i in range(n)]
        remain = 0
        for i in range(n):
            remain = remain * 10 + int(word[i])
            if remain % m == 0:
                div[i] = 1
            else:
                div[i] = 0
            remain = remain % m
        return div
```


## 6367. 求出最多标记下标
> 给你一个下标从 0 开始的整数数组 nums 。一开始，所有下标都没有被标记。你可以执行以下操作任意次：选择两个 互不相同且未标记 的下标 i 和 j ，满足 2 * nums[i] <= nums[j] ，标记下标 i 和 j 。请你执行上述操作任意次，返回 nums 中最多可以标记的下标数目。

这道题的关键点在于，i和j都必须是nums中的下标而且只能出现一次，从贪心的角度来看，nums[i]应该越小越好，nums[j]应该越大越好，所以我们可以先对数组进行排序。同时，这样的下标i和j不会超过n / 2组(其中n是nums的长度)，所以我们可以在排序好后的前n/2个数中找i，在后n/2个数字中找j，这样能找到的结果肯定是最多的。具体的代码如下，时间复杂度是线性的，：


```python
class Solution:
    def maxNumOfMarkedIndices(self, nums: List[int]) -> int:
        nums = sorted(nums)
        n = len(nums)
        m = n // 2
        result = 0
        p = m
        for i in range(m):
            # 原来他妈直接找就可以解决这个问题
            while p < n and nums[i] * 2 > nums[p]:
                p += 1
            if p < n:
                p += 1
                result += 1
            else:
                break
        return result * 2
```