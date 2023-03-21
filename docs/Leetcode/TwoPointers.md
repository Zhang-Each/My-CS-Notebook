# 双指针


## 0011. 盛最多水的容器
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