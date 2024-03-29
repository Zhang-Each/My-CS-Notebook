# 脑筋急转弯

## 0031. 下一个排列
> 给你一个整数数组 nums ，找出 nums 的下一个排列。

这道题的关键在于，要找到那个该变的位置，然后从后面找到一个比这个位置大的数进行交换，交换之后，把那个位置后面的数组从新排序，保证结果是最小的。

```python
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) <= 1:
            return
        i, j, k = len(nums) - 2, len(nums) - 1, len(nums) - 1
        # 找到要换的位置
        while i >= 0 and nums[i] >= nums[j]:
            i -= 1
            j -= 1
        # 找到一个比nums[i]大的换到前面来
        if i >= 0:
            while nums[i] >= nums[k]:
                k -= 1
            nums[i], nums[k] = nums[k], nums[i]
        # 对后面的这一段进行排序，保证结果最小
        nums[j:] = sorted(nums[j:])  
```


## 0448. 找到所有数组中消失的数字 
> 给你一个含 n 个整数的数组 nums ，其中 nums[i] 在区间 [1, n] 内。请你找出所有在 [1, n] 范围内但没有出现在 nums 中的数字，并以数组的形式返回结果。要求不使用除答案以外的额外空间。

不能用额外的空间，可以直接在原本的数字上进行标记，简单有效。

```python
class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        # 直接在原地进行标记
        for i in range(len(nums)):
            nums[abs(nums[i]) - 1] = -abs(nums[abs(nums[i]) - 1])
        result = []
        for i in range(len(nums)):
            if nums[i] > 0:
                result.append(i + 1)
        return result
```

## 1247. 交换字符使得字符串相同
> 有两个长度相同的字符串 s1 和 s2，且它们其中 只含有 字符 "x" 和 "y"，你需要通过「交换字符」的方式使这两个字符串相同。每次「交换字符」的时候，你都可以在两个字符串中各选一个字符进行交换。
> 交换只能发生在两个不同的字符串之间，绝对不能发生在同一个字符串内部。也就是说，我们可以交换 s1[i] 和 s2[j]，但不能交换 s1[i] 和 s1[j]。
> 最后，请你返回使 s1 和 s2 相同的最小交换次数，如果没有方法能够使得这两个字符串相同，则返回 -1 。
> 题目给了一些例子，比如xx和yy交换需要一次，而xy和yx交换需要两次，xx和xy则无法完成交换

首先题目中说的交换只能发生在两个字符串之间，并且为了次数最少，如果s1和s2对应位置上的字符相同，我们肯定是不会去换的，所以我们要统计s1和s2两个字符串对应位置有哪些地方不同，不同的情况可以分成两种，一种是s1上是x而s2上是y，另一种则反之。
我们假设两种情况各有a和b个，那么根据上文所述，我们的交换只能在这些位置上发生。如果a+b是一个奇数，那很明显无法完成交换，因为x和y的总数就不相等，所以我们只需要再考虑a+b是偶数的情况。
因为xx和yy只需要交换一次，所以我们可以尽可能把a对x-y中的xx和yy配对进行交换，这就需要a/2次，同理b对y-x中的yy和xx也可以交换，这就需要b/2次，这时候a和b如果都是偶数，那已经交换完了，如果a和b都是奇数(不可能一奇一偶，因为他们的和是偶数)，那么就还剩一组xy和yx需要交换两次，把这个过程写成代码如下：

```cpp
class Solution {
public:
    int minimumSwap(string s1, string s2) {
        // 其实只要统计xy和yx这样的对的数量就可以
        int a = 0, b = 0;
        for (int i = 0; i < s1.size(); i ++) {
            if (s1[i] != s2[i]) {
                if (s1[i] == 'x') {
                    a ++;
                } else {
                    b ++;
                }
            }
        }
        if ((a + b) % 2 != 0) {
            return -1;
        }
        // a和b都是偶数的时候，刚好能换完
        if(a % 2 == 0 && b % 2 == 0) {
            return (a + b) / 2;
        }
        // a和b都是奇数的时候，要各留一对最后再交换两次
        return (a + b - 2) / 2 + 2;
    }
};
```



## 6360. 最小无法得到的或值
>给你一个下标从 0 开始的整数数组 nums 。
>如果存在一些整数满足 0 <= index1 < index2 < ... < indexk < nums.length ，得到 nums[index1] | nums[index2] | ... | nums[indexk] = x ，那么我们说 x 是 可表达的 。换言之，如果一个整数能由 nums 的某个子序列的或运算得到，那么它就是可表达的。
>请你返回 nums 不可表达的 最小非零整数 。

这道题是个脑筋急转弯的题目，我们可以发现，如果小于等于$2^{i}$的数字都可以被表达，那么$2^{i} +\sim 2^{i + 1} -1$的这些数字都可以被表示，所以不可表达的最小非零整数肯定是2的幂次，并且由于是2的幂次，所以它不能被自己以外的数来表示，因为它的二进制表示中只有一个0，如果其他数想表示我们要找的这个数，那么这些对应位置上必须要是0，所以这个要找的2的幂次肯定在nums数据里面。
现在题目就变成了，找出nums中不存在的最小的2的幂次，代码如下：

```python
class Solution:
    def minImpossibleOR(self, nums: List[int]) -> int:
        # 原来就是一个脑筋急转弯的题目，哈哈
        nums = set(nums)
        i = 0
        while 2 ** i in nums:
            i += 1
        return 2 ** i
```


