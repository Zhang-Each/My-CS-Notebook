# 前缀和

## 6317. 统计美丽子数组数目
> 给你一个下标从 0 开始的整数数组nums 。每次操作中，你可以：
> 1. 选择两个满足 0 <= i, j < nums.length 的不同下标 i 和 j 。
> 2. 选择一个非负整数 k ，满足 nums[i] 和 nums[j] 在二进制下的第 k 位（下标编号从 0 开始）是 1 ,将 nums[i] 和 nums[j] 都减去 2k 。
> 如果一个子数组内执行上述操作若干次后，该子数组可以变成一个全为 0 的数组，那么我们称它是一个 美丽 的子数组。
> 请你返回数组 nums 中 美丽子数组 的数目。子数组是一个数组中一段连续 非空 的元素序列。

统计子数组是前缀和的一种重要应用场景，对于这道题目来说，要满足条件2，那么这一段子数组上每个数组每一位二进制表示按位统计之后，**每一位上出现的次数的和应该都是偶数**，然后我们就可以用前缀和来记录这个统计结果，然后用map存储之间的结果，就可以降低时间的复杂度，然后找出所有的子数组数量。

```python
class Solution:
    def beautifulSubarrays(self, nums: List[int]) -> int:
        # 前缀和+二进制表示
        bins = [bin(num)[2:][::-1] for num in nums]
        n = len(nums)
        prefix = defaultdict(int)
        pos = [0 for i in range(20)]
        count = 0
        prefix[self.serial(pos)] = 1
        for i in range(n):
            num = bins[i]
            for j in range(len(num)):
                pos[j] = (pos[j] + int(num[j])) % 2
            s = self.serial(pos)
            count += prefix[s]
            # print(s)
            prefix[s] += 1
        return count
    
    def serial(self, nums):
        return "".join(str(i) for i in nums)
```


## 9997. 字母与数字
> 给定一个放有字母和数字的数组，找到最长的子数组，且包含的字母和数字的个数相同。返回该子数组，若存在多个最长子数组，返回左端点下标值最小的子数组。若不存在这样的数组，返回一个空数组。

这个题又是**前缀和**的经典应用题，我们可以先把每个数字看成1，每个字符看成-1，这样一来包含的字母和数字的个数相同的子数组**就可以转化成和为0的子数组**，我们记录从0到i的数组的和，保存在字典中，当第二次出现相同的和的时候就可以找到一个符合条件的子数组，然后比较一下是不是最长的就可以了。

```python
class Solution:
    def findLongestSubarray(self, array: List[str]) -> List[str]:
        prefix = {}
        prefix[0] = 0
        res = []
        maxl, count = 0, 0
        # 将问题转化成前缀和的问题
        for i in range(len(array)):
            if array[i].isdigit():
                count += 1
            else:
                count -= 1
            if count not in prefix:
                prefix[count] = i + 1
            else:
                left = prefix[count]
                if i + 1 - left > maxl:
                    maxl = i + 1 - left
                    res = array[left: i + 1]
        return res
```