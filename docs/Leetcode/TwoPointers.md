# 双指针


## 0011.盛最多水的容器
> 给定一个长度为 n 的整数数组 height 。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i]) 。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。

如果在第i和j条线之间构建一个容器，那么容器的宽就是j-i，而容器的高度就是`max(height[i], height[j])`，这时候，如果我们对i进行右移或者对j进行左移，那么宽度一定在减小，而高度的变化情况则可以分类讨论：
- 如果移动i和j中height比较大的那个，那么新容器的高度一定减小，盛水量也一定减小
- 如果移动比较小的那个，那么新容器的高度有可能会增大，盛水量有机会变大
所以我们为了找到最大的容积，可以从两端开始，设置两个指针进行移动，每次将高度较小的那一方进行移动，这样一定能搜索出最大的面积。最终的代码如下：

```cpp
class Solution {
public:
    int maxArea(vector<int>& height) {
        int result = 0, left = 0, right = height.size() - 1;
        while (left < right) {
            int h = min(height[left], height[right]);
            result = max(result, h * (right - left));
            if (height[left] < height[right]) {
                left += 1;
            } else {
                right -= 1;
            }
        }
        return result;
    }
};
```

## 1156.单字符重复子串的最大长度
> 如果字符串中的所有字符都相同，那么这个字符串是单字符重复的字符串。给你一个字符串 text，你只能交换其中两个字符一次或者什么都不做，然后得到一些单字符重复的子串。返回其中最长的子串的长度。

要只交换两个字符一次能实现单字符重复的子串变长，那必须两个子串中间只隔了一个其他字母，基于这一点，我们可以用双指针来遍历字符串，每次找到一堆相隔一个字符的两个单字符重复子串，就可以找出答案，具体的代码如下：

```python
class Solution:
    def maxRepOpt1(self, text: str) -> int:
        mp = defaultdict(int)
        for i in text:
            mp[i] += 1
        n = len(text)
        i = 0
        result = 0
        while i < n:
            j = i
            while j < n and text[j] == text[i]:
                j += 1
            left = j - i
            k = j + 1
            while k < n and text[k] == text[i]:
                k += 1
            right = k - (j + 1)
            result = max(result, min(left + right + 1, mp[text[i]]))
            i = j
        return result
```

## 1574.删除最短的子数组使剩余数组有序
> 给你一个整数数组 arr ，请你删除一个子数组（可以为空），使得 arr 中剩下的元素是非递减 的。
> 一个子数组指的是原数组中连续的一个子序列。
> 请你返回满足题目要求的最短子数组的长度。

经典的双指针问题，因为要拿掉的子数组是连续的，所以只可能出现三种情况：
- 从最左边拿掉一段
- 从最右边拿掉一段
- 从中间拿掉一段
前两种情况，我们可以直接从两端开始遍历，如果出现了数组递减的情况就可以停止，实现的复杂度肯定是$O(N)$的，关键的问题其实就是如何实现第三种情况。
我们可以用双指针法来解决这个问题，从数组的最右端开始往前遍历，先找到一个非递减的序列，假设这个序列初始位置是j，然后我们设定一个下标i从0开始遍历，这就定义好了两个指针，具体的遍历方法是：
- 对于每一个num[i]，我们要判断它能不能接到num[j]的前面，让整个数组非递减
	- 如果可以，那么我们把i-j之间的删除(不包含两端)就是一个答案
	- 如果不可以，我们就应该向右寻找一个合适的j直到他们能够拼在一起，因为如果固定j的位置不变，我们后面找到的新的num[i]肯定会更大(因为这个数组必须非递减)，那么非递减的条件会越来越难以满足，所以j必须要向右移动
- 如果num[i]比后面一个num[i+1]要大，那么搜索就结束了，因为数列必须要非递减
同时我们发现，第三种方法的搜索过程可以涵盖前两种情况，总的时间复杂度由于双指针的存在还是$O(N)$的，具体的代码如下：
```python
class Solution:
    def findLengthOfShortestSubarray(self, arr: List[int]) -> int:
        n = len(arr)
        j = n - 1
        while j > 0:
            if arr[j - 1] <= arr[j]:
                j -= 1
            else:
                break
        result = j
        if result == 0:
            return result
        # 双指针的做法
        for i in range(n):
            while j < n and arr[i] > arr[j]:
                j += 1
            # 删除的部分不包括i和j，所以删除的个数是j-i-1
            result = min(result, j - i - 1)
            if i < n - 1 and arr[i] > arr[i + 1]:
                break
        return result
```