# 贪心算法

## 0135. 分发糖果

> n 个孩子站成一排。给你一个整数数组 ratings 表示每个孩子的评分。你需要按照以下要求，给这些孩子分发糖果：每个孩子至少分配到 1 个糖果。相邻两个孩子评分更高的孩子会获得更多的糖果。请你给每个孩子分发糖果，计算并返回需要准备的 最少糖果数目 。

根据题目要求，分数比旁边高的人获得的糖果也越多，所以我们可以遍历两次，第一次让每个比左边的人分数高的人多分若干个糖果，第二次让每个比右边分数高的人多分若干个糖果，两次遍历后就可以得知每个人需要的糖果数。这个过程中用到了贪心的思路，主要就是把糖果数量降到最小，让每一个人只比周围分数最高的那个人多一个糖果。

```c++
class Solution {
public:
    int candy(vector<int>& ratings) {
        int n = ratings.size();
        vector<int> result(n, 1);
        for (int i = 1; i < n; i ++) {
            if (ratings[i] > ratings[i - 1]) {
                result[i] = result[i - 1] + 1;
            }
        }
        for (int i = n - 2; i >= 0; i --) {
            if (ratings[i] > ratings[i + 1]) {
                result[i] = max(result[i], result[i + 1] + 1);
            }
        }
        int count = 0;
        for (int i = 0; i < n; i ++) {
            count += result[i];
        }
        return count;
    }
};
```


## 0300.最长递增子序列
> 给你一个整数数组 nums ，找到其中最长严格递增子序列的长度。

首先这个题目明显可以用动态规划来解决，两层for循环，复杂度是$O(N^2)$，这个很容易想到，代码如下：

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if len(nums) <= 1:
            return len(nums)
        n = len(nums)
        dp = [1 for i in range(n)]
        for i in range(n):
            for j in range(i):
                if nums[i] > nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```

但是这道题目还可以进一步优化，我们考虑一个很简单的贪心，每次找到新数字加入递增子序列的时候，这个新的数字应该比之前的序列的最后一个数要大，我们为了找到更长的数组，应该希望这个数字尽可能小，所以，用数组d[i]表示长度为i的最长递增子序列的最小末尾数字，然后我们遍历整个数组，进行两步操作：
- 如果当前数字num比d[-1]要大，就把num添加到d的末尾，表示最长递增子序列变长了
- 如果当前数字num比d[-1]要小，那么就要找到num合适的位置，并把d进行更新，同时由于d是单调递增的，因此可以用二分法加快查询
最终的答案就是数组d的长度，因为我们在贪心的过程中，始终不会使得最终的答案变小，所以最后得到的一定是全局最优的答案。具体的代码如下：

```python
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        # d[i]表示长度为i的序列中末尾数最小值
        d = []
        for num in nums:
            if d == [] or num > d[-1]:
                d.append(num)
            else:
                l, r = 0, len(d) - 1
                pos = r
                while l <= r:
                    mid = (l + r) // 2
                    if d[mid] >= num:
                        pos = mid
                        r = mid - 1
                    else:
                        l = mid + 1
                d[pos] = num
        return len(d)
```