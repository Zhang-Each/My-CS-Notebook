# 深度优先搜索

## 0200. 岛屿数量
> 给你一个由 '1'（陆地）和 '0'（水）组成的的二维网格，请你计算网格中岛屿的数量。岛屿总是被水包围，并且每座岛屿只能由水平方向和/或竖直方向上相邻的陆地连接形成。
> 此外，你可以假设该网格的四条边均被水包围。

由于连成一块的1只能算1个岛屿，所以我们在碰到1的时候，要将和这个1相连的1全部消除，这样就算遍历了一个岛屿，遍历完所有的grid之后，岛屿的数量就统计出来了。

```c++
class Solution {
public:
    int numIslands(vector<vector<char>>& grid) {
        int count = 0, m = grid.size(), n = grid[0].size();
        for (int i = 0; i < m; i ++) {
            for (int j = 0; j < n; j ++) {
                if (grid[i][j] == '1') {
                    count += 1;
                    dfs(grid, i, j);
                }
            }
        }
        return count;
    }

    void dfs(vector<vector<char>>& grid, int i, int j) {
        if (i < 0 || j < 0 || i >= grid.size() || j >= grid[i].size()) {
            return;
        }
        if (grid[i][j] == '0') {
            return;
        }
        grid[i][j] = '0';
        dfs(grid, i + 1, j);
        dfs(grid, i - 1, j);
        dfs(grid, i, j + 1);
        dfs(grid, i, j - 1);
    }
};
```