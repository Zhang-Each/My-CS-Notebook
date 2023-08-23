# 动态规划

## 0005. 最长回文子串
> 给你一个字符串 s，找到 s 中最长的回文子串。如果字符串的反序与原始字符串相同，则该字符串称为回文字符串。

经典的动态规划问题，用一个数组`dp[i][j]`表示s从i到j这一段是不是回文字符串，dp的情况可以分成下面几种：
- 如果`i == j` 那么很明显是的
- 如果`i + 1 == j` 那么就看`s[i + 1] == s[j]`是否成立
- 其他情况，要先判断`s[i + 1] == s[j - 1]`是否成立，然后再根据`dp[i + 1][j - 1]`是不是1来决定`dp[i][j]`的结果
同时，因为遍历过程中，需要知道i+1的情况，所以第一层关于i的循环要倒着进行，保证`dp[i + 1][j - 1]`是一个有效值。具体的代码如下：

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[0 for i in range(n)] for j in range(n)]
        maxl = 1
        res = s[0]
        # 经典dp，经典中的经典
        for i in range(n - 1, -1, -1):
            dp[i][i] = 1
            for j in range(i + 1, n):
                if j == i + 1:
                    dp[i][j] = 1 if (s[i] == s[j]) else 0
                else:
                    if s[i] == s[j]:
                        dp[i][j] = dp[i + 1][j - 1]
                    else:
                        dp[i][j] = 0
                if dp[i][j] and j - i + 1 > maxl:
                    maxl = j - i + 1
                    res = s[i: j + 1]
        return res

```


## 1105.填充书架
> 给定一个数组 books ，其中 books[i] = [thicknessi, heighti] 表示第 i 本书的厚度和高度。你也会得到一个整数 shelfWidth 。按顺序 将这些书摆放到总宽度为 shelfWidth 的书架上。先选几本书放在书架上（它们的厚度之和小于等于书架的宽度 shelfWidth ），然后再建一层书架。重复这个过程，直到把所有的书都放在书架上。
> 需要注意的是，在上述过程的每个步骤中，摆放书的顺序与你整理好的顺序相同。
> 以这种方式布置书架，返回书架整体可能的最小高度。

很经典的dp问题，首先books必须按顺序摆放，这才使得我们可以使用dp，然后dp的具体方式就是对于每一个下标i，我们找到一个小于i的下标j，使得前j-1本书摆好之后，第j到第i本书另外放置一层，然后更新dp数组，这样就可以完成dp，具体的代码如下：

```python
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        # dp[i] 来表示放下前i本书所用的最小高度
        n = len(books)
        dp = [999999999] * (n + 1)
        dp[0] = 0
        for i in range(n):
            b = books[i]
            width = 0
            height = 0
            j = i
            # 向前进行调整
            while j >= 0:
                width += books[j][0]
                if width > shelfWidth:
                    break
                height = max(height, books[j][1])
                # 前j-1个的结果加上j-i个放成一排后的结果
                dp[i + 1] = min(dp[i + 1], dp[j] + height)
                j -= 1
        return dp[-1]
```


## 1335.工作计划的最低难度
> 你需要制定一份 d 天的工作计划表。工作之间存在依赖，要想执行第 i 项工作，你必须完成全部 j 项工作（ 0 <= j < i）。你每天 至少 需要完成一项任务。工作计划的总难度是这 d 天每一天的难度之和，而一天的工作难度是当天应该完成工作的最大难度。
> 给你一个整数数组 jobDifficulty 和一个整数 d，分别代表工作难度和需要计划的天数。第 i 项工作的难度是 jobDifficulty[i]。
> 返回整个工作计划的 最小难度 。如果无法制定工作计划，则返回 -1 

首先每天至少要完成一项工作，所以如果jobDifficulty的长度小于d那就无法制定工作计划。然后我们仔细分析题意就会发现，实际上我们是需要将jobDifficulty分成d份，然后求出这d份的每一份中元素最大值的最小值(即难度)，所以我们可以考虑用dp或者记忆化搜索，用`dfs(i, day)`表示从第i天开始，将剩余工作安排在day日完成的最小难度，实现记忆化搜索的代码如下：

```python
class Solution:
    def minDifficulty(self, jobDifficulty: List[int], d: int) -> int:
        n = len(jobDifficulty)
        if n < d:
            return -1
        
        # dfs(i, day)表示从第i个工作开始做day天的最小工作量
        @cache
        def dfs(i, day):
            if day == 1:
                return max(jobDifficulty[i:])
            # 把i-j的固定为一天然后开始搜索
            return min(max(jobDifficulty[i: j]) + dfs(j, day - 1) for j in range(i + 1, n - day + 2))
        
        return dfs(0, d)

```


## 1653. 使字符串平衡的最少删除次数
> 给你一个字符串 s ，它仅包含字符 'a' 和 'b'​​​​ 。你可以删除 s 中任意数目的字符，使得 s 平衡 。当不存在下标对 (i,j) 满足 i < j ，且 s[i] = 'b' 的同时 s[j]= 'a' ，此时认为 s 是 平衡 的。
> 请你返回使 s 平衡 的 最少 删除次数。

这道题目的意思非常明确，就是要把字符串s处理成前面全是a后面全是b的形式(当然a和b可以没有)
我们可以将这个问题转化成一个DP问题，用dp表示字符串s的最少删除次数，如果我们在s尾部新增一个字符，那么dp的更新可以分成两种情况讨论：
- 如果新增了一个a，我们可以把这个a删除，或者把前面的b全部删除，我们需要记录前面b的个数
- 如果新增了一个b，因为前面的字符串已经平衡了，所以可以先记录b的数量，不需要进行删除操作
最终的代码如下：

```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        # 所有的a必须出现在所有的b前面，当然a也可以没有
        count = 0
        dp = 0
        for i in s:
            # 简单动态规划，如果最后是a，要不就删除，要不就把前面的b全部删除
            if i == 'a':
                dp = min(dp + 1, count)
            else:
                count += 1
        return dp
```



## 6310. 获得分数的方法数
> 考试中有 n 种类型的题目。给你一个整数 target 和一个下标从 0 开始的二维整数数组 types ，其中 types[i] = [counti, marksi] 表示第 i 种类型的题目有 counti 道，每道题目对应 marksi 分。
> 返回你在考试中恰好得到 target 分的方法数。由于答案可能很大，结果需要对 109 +7 取余。

这道题是一道很经典的dp计数的题目，我们可以开一个长度为target+1的数组dp，dp[i]代表了分数恰好为i的时候的方案总数，并遍历types数组，对可以获得的分数进行dp，具体的代码如下：

```python
class Solution:
    def waysToReachTarget(self, target: int, types: List[List[int]]) -> int:
        dp = [0 for i in range(target + 1)]
        mod = 10 ** 9 + 7
        dp[0] = 1
        # 直接dp居然真的可以过，惊了
        for tp in types:
            c, m = tp
            for i in range(target, -1, -1):
                for j in range(1, min(c, i // m) + 1):
                    dp[i] = (dp[i] + dp[i - j * m]) % mod
        return dp[-1]
```


## 6433. 矩阵中移动的最大次数
> 给你一个下标从 0 开始、大小为 m x n 的矩阵 grid ，矩阵由若干 正 整数组成。你可以从矩阵第一列中的 任一 单元格出发，按以下方式遍历 grid ：
> 从单元格 (row, col) 可以移动到 (row - 1, col + 1)、(row, col + 1) 和 (row + 1, col + 1) 三个单元格中任一满足值 严格 大于当前单元格的单元格。
> 返回你在矩阵中能够 移动 的 最大 次数。

很明显的dp，但是要注意必须要从第一列出发，所以后面的每一列不仅要看前一列是否严格限于，还要看前面一列dp过来的位置是否有效。

```python
class Solution:
    def countCompleteComponents(self, n: int, edges: List[List[int]]) -> int:
        g = [[0 for i in range(n)] for j in range(n)]
        for edge in edges:
            a, b = edge
            g[a][b] = 1
            g[b][a] = 1
        visit = set()
        count = 0
        comps = []
        
        def dfs(i, comp):
            visit.add(i)
            comp.append(i)
            for j in range(len(g[i])):
                if j not in visit and g[i][j] == 1:
                    dfs(j, comp)
            
            
        for i in range(n):
            if i not in visit:
                comp = []
                dfs(i, comp)
                comps.append(comp)
        for comp in comps:
            l = len(comp)
            flag = 1
            for i in range(l):
                for j in range(i + 1, l):
                    if g[comp[i]][comp[j]] == 0:
                        flag = 0
            count += flag
        return count
```



## 6449. 收集巧克力
> 给你一个长度为 n 、下标从 0 开始的整数数组 nums ，表示收集不同巧克力的成本。每个巧克力都对应一个不同的类型，最初，位于下标 i 的巧克力就对应第 i 个类型。在一步操作中，你可以用成本 x 执行下述行为：
> 同时对于所有下标 0 <= i < n - 1 进行以下操作， 将下标 i 处的巧克力的类型更改为下标 (i + 1) 处的巧克力对应的类型。如果 i == n - 1 ，则该巧克力的类型将会变更为下标 0 处巧克力对应的类型。
> 假设你可以执行任意次操作，请返回收集所有类型巧克力所需的最小成本。

可以发现我们最多进行n次下标转移的操作，就一定能找到最合适的方法，假设进行的转移次数是i，那么我们转移需要的成本就是x乘以i，我们接下来只要对每个巧克力j，选出右边i步以内最小的成本，再求和，就是移动i次最少的成本和，为了减小时间复杂度，我们可以用`dp[i][j]`来记录巧克力i距离j以内的最小成本，最终的代码如下：

```python
class Solution:
    def minCost(self, nums: List[int], x: int) -> int:
        n = len(nums)
        dp = [[0 for i in range(n)] for j in range(n)]
        for i in range(n):
            dp[i][0] = nums[i]
            for j in range(1, n):
                k = (i + j) % n
                dp[i][j] = min(dp[i][j - 1], nums[k])
        result = sum(nums)
        # 调整1-n-1次，找出最小的结果
        for i in range(1, n):
            temp = i * x
            for j in range(n):
                temp += dp[j][i]
            result = min(result, temp)
        return result
                
```


## 6898.字符串连接删减字母
> 给你一个下标从 0 开始的数组 words ，它包含 n 个字符串。
> 定义 连接 操作 join(x, y) 表示将字符串 x 和 y 连在一起，得到 xy 。如果 x 的最后一个字符与 y 的第一个字符相等，连接后两个字符中的一个会被 删除 。
> 比方说 join("ab", "ba") = "aba" ， join("ab", "cde") = "abcde" 。
> 你需要执行 n - 1 次 连接 操作。令 str0 = words[0] ，从 i = 1 直到 i = n - 1 ，对于第 i 个操作，你可以执行以下操作之一：
> 令 stri = join(stri - 1, words[i])
> 令 stri = join(words[i], stri - 1)
> 你的任务是使 strn - 1 的长度 最小 。
> 请你返回一个整数，表示 str n - 1 的最小长度。

这道题乍一看回溯就可以解决，但是由于搜索空间很大，所以会超时。我们可以发现，这个join操作，不管是正向还是反向，最终能否触发合并长度-1，都只和每个words[i]的第一个字母和最后一个字母有关，我们可以考虑对首尾字母进行dp，假设`dp[i][j][k]` 表示words前i个单词进行join之后，首位为j而且末尾为k的字符串最小长度，这样一来，对于下一个新的单词，我们考察它能否和`dp[i][j][k]` 合并并发生缩短操作就可以，具体的实现方式有下面两种，一种是递归DFS，一种是dp

```python
class Solution:
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        @cache
        def dfs(i: int, s: str, e: str) -> int:
            if i == n:
                return 0
            t = words[i]
            # 两种情况，分别讨论
            choice1 = dfs(i + 1, s, t[-1]) + len(t) - int(t[0] == e)
            choice2 = dfs(i + 1, t[0], e) + len(t) - int(t[-1] == s)
            result = min(choice1, choice2)
            return result

        n = len(words)
        return dfs(1, words[0][0], words[0][-1]) + len(words[0])


# 另一个dp的做法
class Solution:
    def minimizeConcatenatedLength(self, words: List[str]) -> int:
        n = len(words)
        dp = [[[10 ** 9 for i in range(26)] for j in range(26)] for k in range(n)]
        x0, y0 = ord(words[0][0]) - ord('a'), ord(words[0][-1]) - ord('a')
        dp[0][x0][y0] = len(words[0])
        for i in range(1, n):
            l = len(words[i])
            xi, yi = ord(words[i][0]) - ord('a'), ord(words[i][-1]) - ord('a')
            for j in range(26):
                for k in range(26):
                    if yi == j:
                        dp[i][xi][k] = min(dp[i][xi][k], dp[i - 1][j][k] + l - 1)
                    else:
                        dp[i][xi][k] = min(dp[i][xi][k], dp[i - 1][j][k] + l)
                    if xi == k:
                        dp[i][j][yi] = min(dp[i][j][yi], dp[i - 1][j][k] + l - 1)
                    else:
                        dp[i][j][yi] = min(dp[i][j][yi], dp[i - 1][j][k] + l)
        result = 10 ** 9
        for i in range(26):
            for j in range(26):
                result = min(result, dp[n - 1][i][j])
        return result


```


## 6931.访问数组中的位置使分数最大
> 给你一个下标从 0 开始的整数数组 nums 和一个正整数 x 。你 一开始 在数组的位置 0 处，你可以按照下述规则访问数组中的其他位置：
> 如果你当前在位置 i ，那么你可以移动到满足 i < j 的 任意 位置 j 。
> 对于你访问的位置 i ，你可以获得分数 nums[i] 。
> 如果你从位置 i 移动到位置 j 且 nums[i] 和 nums[j] 的 奇偶性 不同，那么你将失去分数 x 。请你返回你能得到的 最大 得分之和。
> 注意 ，你一开始的分数为 nums[0] 。

乍一看这道题很简单，我们只要用dp+两层循环就能很轻松解决，但实际上这道题数据量比较大，所以有时间复杂度上的要求，我们可以想办法把时间复杂度降低成线性的。具体来说，我们用s[i]表示nums前i项以偶数结尾的最大得分和，用t[i]表示nums前i项以奇数结尾的最大得分和，然后遍历一次nums，根据nums[i]的奇偶性，分别来更新s[i]和t[i]


```python
class Solution:
    def maxScore(self, nums: List[int], x: int) -> int:
        # 分奇偶的动态规划题
        n = len(nums)
        s = [0 for i in range(n)]
        t = [0 for i in range(n)]
        if nums[0] % 2 == 0:
            s[0] = nums[0]
            t[0] = -x
        else:
            s[0] = -x
            t[0] = nums[0]
        for i in range(1, n):
            if nums[i] % 2 == 0:
                s[i] = max(s[i - 1] + nums[i], t[i - 1] + nums[i] - x)
                t[i] = t[i - 1]
            else:
                s[i] = s[i - 1]
                t[i] = max(t[i - 1] + nums[i], s[i - 1] + nums[i] - x)
        return max(max(s), max(t))
```
