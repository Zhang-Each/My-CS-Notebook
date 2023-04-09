# 数组操作题

## 0152. 乘积最大子数组

> 给你一个整数数组 nums ，请你找出数组中乘积最大的非空连续子数组（该子数组中至少包含一个数字），并返回该子数组所对应的乘积。
> 测试用例的答案是一个 32-位 整数。子数组 是数组的连续子序列。

找到连续子数组的最大乘积的关键在于怎么处理负数，因为如果前面几个数字乘出来非常大，但是紧接着来了一个负数，那么这个结果可能就非常小了，但是如果后面再有一个负数，这个乘积可能又会非常大，所以我们要在记录最大值的同时也记录其中的最小值，并且在适当的时候将他们对换，这样遍历一次就可以获得乘积最大的结果。

```python
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        result = nums[0]
        # 分别记录最小的和最大的，涉及到负数的时候就可以转换
        maxp, minp = 1, 1
        for num in nums:
            if num < 0:
                maxp, minp = minp, maxp
            maxp = max(maxp * num, num)
            minp = min(minp * num, num)
            result = max(result, maxp)
        return result
```


## 0982. 按位与为零的三元组
>给你一个整数数组 nums ，返回其中 按位与三元组 的数目。按位与三元组 是由下标 (i, j, k) 组成的三元组，并满足下述全部条件：0 <= i < nums.length, 0 <= j < nums.length, 0 <= k < nums.length, nums[i] & nums[j] & nums[k] == 0 ，其中 & 表示按位与运算符。

- 直接三层循环暴力计算会超时，可以先对nums[i]&nums[j]的结果进行预处理，这样可以把时间复杂度降低成$O(N^2)$

```python
class Solution:
    def countTriplets(self, nums: List[int]) -> int:
        bits = defaultdict(int)
        n = range(len(nums))
        for i in n:
            for j in n:
                bits[nums[i] & nums[j]] += 1
        # 先进行预处理，然后再遍历一轮
        result = 0
        for bit in bits:
            for num in nums:
                if bit & num == 0:
                    result += bits[bit]
        return result
```


## 1144. 递减元素使数组呈锯齿状
> 给你一个整数数组 nums，每次 操作 会从中选择一个元素并 将该元素的值减少 1。如果符合下列情况之一，则数组 A 就是 锯齿数组：每个偶数索引对应的元素都大于相邻的元素，即 A[0] > A[1] < A[2] > A[3] < A[4] > ...或者，每个奇数索引对应的元素都大于相邻的元素，即 A[0] < A[1] > A[2] < A[3] > A[4] < ...
> 返回将数组 nums 转换为锯齿数组所需的最小操作次数。

这道题的关键就在于要发现，数组其实只要调整偶数位或者奇数位置上的那些数字就可以了。比如说，我们要调整使得偶数索引对应的元素都大于相邻的元素，那么我们对每个偶数索引对应的元素，都要把它们调整到max(a, b) + 1(其中a和b是它左右两个相邻的数字)才能满足条件，如果我们对a和b也进行调整，我们可以分情况讨论，如果调整后max(a, b)的值没有变或者变大了，那么显然是做了无用功，如果max(a, b)变小了，那么虽然我们对偶数索引的数的调整可能变少了，但是总体来看，我们还是多调整了a或者b，导致实际的操作次数没有发生变化，所以我们只需要调整每一个偶数索引即可，而不需要调整奇数索引上的数字。如果要把数组调整成另一种情况也是同理，所以我们只要比较一下两种情况下分别需要的最小操作次数就可以了。

```cpp
class Solution {
public:
    int movesToMakeZigzag(vector<int>& nums) {
        // 只调整奇数部分或者只调整偶数部分，不然工作量肯定会增大
        int a = 0, b = 0;
        for (int i = 0; i < nums.size(); i += 2) {
            // 让偶数部分更大
            int s = 0;
            if (i - 1 >= 0) {
                s = max(s, nums[i] - nums[i - 1] + 1);
            }
            if (i + 1 < nums.size()) {
                s = max(s, nums[i] - nums[i + 1] + 1);
            }
            a += s;
        }
        for (int i = 1; i < nums.size(); i += 2) {
            int s = 0;
            if (i - 1 >= 0) {
                s = max(s, nums[i] - nums[i - 1] + 1);
            }
            if (i + 1 < nums.size()) {
                s = max(s, nums[i] - nums[i + 1] + 1);
            }
            b += s;
        }
        return min(a, b);
    }
};
```


## 1590. 使数组和能被 P 整除
> 给你一个正整数数组 nums，请你移除 最短 子数组（可以为 空），使得剩余元素的 和 能被 p 整除。 不允许 将整个数组都移除。
> 请你返回你需要移除的最短子数组的长度，如果无法满足题目要求，返回 -1 。

剩下元素的和能被p整除说明子数组除以p的余数应该和整个数组相同，我们可以先求出这个余数，然后使用hash+一次循环来找出最短的子数组，感觉是非常经典的题目。

```python
class Solution {
public:
    int minSubarray(vector<int>& nums, int p) {
        int target = 0, result = nums.size(), sum = 0;
        for (int i = 0; i < nums.size(); i ++) {
            target = (target + nums[i]) % p;
        }
        if (target == 0) {
            return 0;
        }
        unordered_map<int, int> pos;
        pos[0] = -1;
        for (int i = 0; i < nums.size(); i ++) {
            sum = (sum + nums[i]) % p;
            int mod = (sum - target + p) % p;
            pos[sum] = i;
            if (pos.find(mod) != pos.end()) {
                result = min(result, i - pos[mod]);
            }
        }
        if (result == nums.size()) {
            return -1;
        }
        return result;
    }
};
```



## 6309. 分割数组使乘积互质
> 给你一个长度为 n 的整数数组 nums ，下标从 0 开始。如果在下标 i 处 分割 数组，其中 0 <= i <= n - 2 ，使前 i + 1 个元素的乘积和剩余元素的乘积互质，则认为该分割 有效 。返回可以有效分割数组的最小下标 i ，如果不存在有效分割，则返回 -1 。

这道题的关键在于：分割后的左右两部分，**左边的任意一个数和右边的任意一个数应该是互质的**，如果不是，那么这个分割就是无效的，因为左右两边的乘积也不会互质。我们可以设置一个offset代表最合适的分割点，并且这个分割点会不断更新。
我们从最左边开始遍历数组，对于每个nums[i]，从数组最后开始找到第一个与它不互斥的数nums[j]，这样一来，offset就不会小于j，否则无法满足上面的条件，这样一来我们可以确保，对于当前的i，offset后面的所有数字都和0-i之间的所有数字互斥，当i和offset重合的时候，就说明我们找到了最合适的分割点。

```python
import math


class Solution:
    def findValidSplit(self, nums: List[int]) -> int:
        # 核心是让左右两边的数组都互质
        if len(nums) == 1:
            return -1
        offset = 0
        n = len(nums)
        for i in range(n):
            for j in range(n - 1, offset, -1):
                gcd = math.gcd(nums[i], nums[j])
                if gcd != 1:
                    if j == n - 1:
                        return -1
                    offset = j
                    break
            if i == offset:
                return offset
        return -1
```


## 6313. 统计将重叠区间合并成组的方案数
> 给你一个二维整数数组 ranges ，其中 ranges[i] = [starti, endi] 表示 starti 到 endi 之间（包括二者）的所有整数都包含在第 i 个区间中。你需要将 ranges 分成 两个 组（可以为空），满足：每个区间只属于一个组。两个有交集的区间必须在 同一个组内。如果两个区间有至少 一个 公共整数，那么这两个区间是有交集的。
> 比方说，区间 [1, 3] 和 [2, 5] 有交集，因为 2 和 3 在两个区间中都被包含。请你返回将 ranges 划分成两个组的总方案数 。

由于两个有交集的区间必须要分在一起，我们可以把整个ranges数组划分成K个集合，每个集合包含了若干区间，集合内的区间互有交集，集合间互相没有交集，这样一来，每个集合里的range必须出现在同一个组里，但是不同集合之间没有硬性的约束，这样一来，总的方案数量实际就是$2^K$，因为K个集合可以分到任意一个组中。
剩下的问题就在于如何计算K的数量，我们可以先对ranges数组先排序，然后遍历一次就可以计算出不相交的区间集合K的总数，具体的代码如下：

```python
class Solution:
    def countWays(self, ranges: List[List[int]]) -> int:
        count = 1
        ranges = sorted(ranges, key=lambda x: (x[0], x[1]))
        left, right = ranges[0]
        # 主要是统计有多少组必须分到一起的区间，假设这个数是n，那最后的结果就是2**n
        for i in range(1, len(ranges)):
            b = ranges[i]
            if b[0] > right:
                left, right = b[0], b[1]
                count += 1
            else:
                right = max(right, b[1])
        return 2 ** count % (10 ** 9 + 7)

```

## 6325. 修车的最少时间
> 给你一个整数数组 ranks ，表示一些机械工的 能力值 。ranksi 是第 i 位机械工的能力值。能力值为 r 的机械工可以在 r * n2 分钟内修好 n 辆车。
> 同时给你一个整数 cars ，表示总共需要修理的汽车数目。
> 请你返回修理所有汽车 最少 需要多少时间。
> 注意：所有机械工可以同时修理汽车。

这道题的解法居然是对时间进行二分然后判断这个时间能不能修完，大受震撼。
```python
class Solution:
    def repairCars(self, ranks: List[int], cars: int) -> int:
        # 居然是二分法，两眼一黑
        s = lambda t: sum(floor((t // r) ** 0.5) for r in ranks)
        return bisect_left(range(min(ranks) * cars * cars), cars, key=s)
```


## 6329. 使子数组元素和相等
> 给你一个下标从 0 开始的整数数组 arr 和一个整数 k 。数组 arr 是一个循环数组。换句话说，数组中的最后一个元素的下一个元素是数组中的第一个元素，数组中第一个元素的前一个元素是数组中的最后一个元素。
> 你可以执行下述运算任意次：
> 选中 arr 中任意一个元素，并使其值加上 1 或减去 1 。
> 执行运算使每个长度为 k 的 子数组 的元素总和都相等，返回所需要的最少运算次数。
> 子数组 是数组的一个连续部分。

要长度为k的子数组相等，就必须让数组里所有相距k个位置两两相等，然后一圈轮下来会有很多重合的地方，至于哪些位置会重合，这个跟k和len(arr)的最大公约数有关，在我们把arr划分成若干个组后，每个组内的每个数字就必须相等，这个可以先中位数然后计算最小的操作次数，最终的代码如下：

```python
class Solution:
    def makeSubKSumEqual(self, arr: List[int], k: int) -> int:
        n = len(arr)
        def gcd(a, b):
            if b == 0:
                return a
            return gcd(b, a % b)
        
        g = gcd(n, k)
        nums = [[] for i in range(g)]
        result = 0
        for i in range(n):
            nums[i % g].append(arr[i])
        for i in range(g):
            result += self.find(nums[i])
        return result
    
    def find(self, nums):
        nums = sorted(nums)
        n = len(nums)
        if n % 2 == 1:
            median = nums[n // 2]
            return sum(abs(num - median) for num in nums)
        else:
            median1, median2 = nums[n // 2 - 1], nums[n // 2]
            return min(sum(abs(num - median1) for num in nums), sum(abs(num - median2) for num in nums))
        
        
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


