# 数据结构-堆

## 0215. 数组中的第K个最大元素
> 给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

- 找第K大的数字最简单的方法就是用堆

```python
import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        k = len(nums) - k
        heapq.heapify(nums)
        while k > 0:
            heapq.heappop(nums)
            k -= 1
        result = heapq.heappop(nums)
        return result
```


## 1439. 有序矩阵中的第 k 个最小数组和
> 给你一个 m * n 的矩阵 mat，以及一个整数 k ，矩阵中的每一行都以非递减的顺序排列。
> 你可以从每一行中选出 1 个元素形成一个数组。返回所有可能数组中的第 k 个 最小 数组和。

这道题可以直接用暴力方法解决，但是比较慢，虽然这道题数据量不大，勉强可以通过。碰到第k个最小这样的表述时，我们可以考虑用堆来优化我们的算法。
在这道题中，我们可以将m行一行行进行处理，每次考虑两行的第k个最小和，然后用堆来帮助我们找到最小的第k个，这么搞就不用遍历整个数组。

```python
class Solution:
    def kthSmallest(self, mat: List[List[int]], k: int) -> int:
        
        def merge(f, g, k):
            if len(g) < len(f):
                return merge(g, f, k)
            # 用堆进行优化
            q =[(f[0] + g[i], 0, i) for i in range(len(g))]
            heapq.heapify(q)
            result = []
            while k > 0 and q:
                v, i, j = heapq.heappop(q)
                result.append(v)
                if i + 1 < len(f):
                    heapq.heappush(q, (f[i + 1] + g[j], i + 1, j))
                k -= 1
            return result
        

        arr = mat[0]
        for i in range(1, len(mat)):
            arr = merge(arr, mat[i], k)
        return arr[-1]
```