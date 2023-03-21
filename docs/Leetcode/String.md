
## 1487. 保证文件名唯一
> 给你一个长度为 n 的字符串数组 names 。你将会在文件系统中创建 n 个文件夹：在第 i 分钟，新建名为 names[i] 的文件夹。由于两个文件 不能 共享相同的文件名，因此如果新建文件夹使用的文件名已经被占用，系统会以 (k) 的形式为新文件夹的文件名添加后缀，其中 k 是能保证文件名唯一的 最小正整数 。返回长度为 n 的字符串数组，其中 ans[i] 是创建第 i 个文件夹时系统分配给该文件夹的实际名称。

- 用一个map保存每个文件名对应的相同文件的个数，然后直接开始搜就可以了

```python
class Solution:
    def getFolderNames(self, names: List[str]) -> List[str]:
        result, mp = [], {}
        for name in names:
            s = name
            # 直接开始搜索就行
            while s in mp:
                s = "{}({})".format(name, mp[name])
                mp[name] += 1
            mp[s] = 1
            result.append(s)
        return result
```


## 1616. 分割两个字符串得到回文串
> 给你两个字符串 a 和 b ，它们长度相同。请你选择一个下标，将两个字符串都在 相同的下标 分割开。由 a 可以得到两个字符串： aprefix 和 asuffix ，满足 a = aprefix + asuffix ，同理，由 b 可以得到两个字符串 bprefix 和 bsuffix ，满足 b = bprefix + bsuffix 。请你判断 aprefix + bsuffix 或者 bprefix + asuffix 能否构成回文串。
> 当你将一个字符串 s 分割成 sprefix 和 ssuffix 时， ssuffix 或者 sprefix 可以为空。比方说， s = "abc" 那么 "" + "abc" ， "a" + "bc" ， "ab" + "c" 和 "abc" + "" 都是合法分割。

这道题的关键在于发现这样两点：
1. aprefix + bsuffix和bprefix + asuffix实际上是等价的，我们只要调换一下a和b的顺序就可以将这两者互相进行转换，所以我们只要判断aprefix + bsuffix是不是回文就可以了
2. aprefix + bsuffix的左端必定在a的左端，而右端必定在b的右端，所以我们可以从a和b的两端分别开始遍历，把能够成回文的先找出来，假设a[0: i]和b[j+1:]构成回文字符串，如果i不小于j，那么我们已经找到了符合条件的(要注意两个字符串都只能在同一个位置切开)，否则，我们就要判断a[i: j + 1]或者b[i: j + 1]是否有可能构成回文字符串，因为这时候从a和b各选一个已经不行了，所以只能从一个字符串那里选。

```python
class Solution:
    def checkPalindromeFormation(self, a: str, b: str) -> bool:
        return self.checkPalidrome(a, b) or self.checkPalidrome(b, a)
    

    def checkPalidrome(self, a, b):
        n = len(a)
        left, right = 0, n - 1
        while left < right and a[left] == b[right]:
            left += 1
            right -= 1
        if left >= right:
            return True
        x, y = a[left: right + 1], b[left: right + 1]
        return x == x[::-1] or y == y[::-1]
```