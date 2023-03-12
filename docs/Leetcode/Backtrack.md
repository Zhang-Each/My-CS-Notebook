# 回溯算法

## 0046. 全排列

> 给定一个不含重复数字的数组 nums ，返回其 所有可能的全排列 。你可以 按任意顺序 返回答案。

经典的回溯问题，用一个visit数组记录遍历的情况，然后用一个循环，从每一个num开始轮流遍历，这样就可以遍历所有的排列情况

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        def dfs(temp, visit, nums):
            n = len(nums)
            if len(temp) == n:
                result.append(temp.copy())
                return
            for i in range(n):
                if visit[i] == 0:
                    visit[i] = 1
                    temp.append(nums[i])
                    dfs(temp, visit, nums)
                    temp.pop(-1)
                    visit[i] = 0
                else:
                    continue
        
        visit = [0 for num in nums]
        dfs([], visit, nums)
        return result
```