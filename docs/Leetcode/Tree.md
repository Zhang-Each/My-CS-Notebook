# 数据结构-树

## 6308. 二叉树中的第 K 大层和
> 给你一棵二叉树的根节点 root 和一个正整数 k 。树中的 层和 是指 同一层 上节点值的总和。返回树中第 k 大的层和（不一定不同）。如果树少于 k 层，则返回 -1 。注意，如果两个节点与根节点的距离相同，则认为它们在同一层。

经典的层序遍历模版题，记住层序遍历的模版就可以了

```python
class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        q = [(root, 0)]
        mp = defaultdict(int)
        while len(q) != 0:
            p, l = q[0]
            q.pop(0)
            if p.left is not None:
                q.append((p.left, l + 1))
            if p.right is not None:
                q.append((p.right, l + 1))
            mp[l] += p.val
        sums = sorted(mp.values())[::-1]
        return sums[k - 1] if k <= len(sums) else -1
```