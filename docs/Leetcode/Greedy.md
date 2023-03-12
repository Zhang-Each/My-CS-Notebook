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
