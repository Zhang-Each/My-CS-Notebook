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