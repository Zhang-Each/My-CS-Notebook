# 数据结构-栈

## 0739.每日温度
> 给定一个整数数组 temperatures ，表示每天的温度，返回一个数组 answer ，其中 answer[i] 是指对于第 i 天，下一个更高温度出现在几天后。如果气温在这之后都不会升高，请在该位置用 0 来代替。

经典的单调栈问题，用一个栈记录前面没确定下一个最高温的元素，然后遍历整个数组，每到一处就把能安排的全安排了就行。

```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        stack = []
        n = len(temperatures)
        result = [0 for i in range(n)]
        # 单调栈的做法
        for i in range(n):
            if stack:
                while stack and temperatures[stack[-1]] < temperatures[i]:
                    result[stack[-1]] = i - stack[-1]
                    stack.pop(-1)
            stack.append(i)
        return result
```