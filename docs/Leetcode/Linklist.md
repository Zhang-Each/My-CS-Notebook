# 数据结构-链表

## 0141. 环形链表
> 给你一个链表的头节点 head ，判断链表中是否有环。如果链表中有某个节点，可以通过连续跟踪 next 指针再次到达，则链表中存在环。 为了表示给定链表中的环，评测系统内部使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。注意：pos 不作为参数进行传递 。仅仅是为了标识链表的实际情况。
> 如果链表中存在环 ，则返回 true 。 否则，返回 false 。

经典的链表题，最简单的方法使用set记录所有的节点，如果出现了重复就说明链表中有环，但是如果要空间复杂度为`O(1)`的话，可以用两个指针，一个每次前进两格，一个每次前进一格，如果他们能相遇就说明链表中存在环。具体的代码如下：

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        if head is None or head.next is None:
            return False
        p, q = head, head
        while p is not None and q is not None:
            p = p.next
            q = q.next
            if q is None:
                return False
            else:
                q = q.next
            if p == q:
                return True
        return False
```


## 0148. 排序链表
> 给你链表的头结点 head ，请将其按 升序 排列并返回 排序后的链表 。

看起来要给链表排序并不难，最简单的做法就是把链表里的数读出来，然后sort一下再放回去，但这么写很明显过不了面试，因为题目的要求是时间复杂度$O(N\log N)$级别同时空间复杂度$O(1)$级别，这就要求我们在原地进行排序，一个很经典的做法就是归并，可问题是两个链表的归并我们会做，那么一个链表该怎么归并呢？
答案是没有两个就创造两个，通过取链表中间节点，将链表分成两段，然后用递归的方式完成归并，实际上在链表中取中间节点也是一个比较常见的trick，用快慢指针法可以实现。具体代码如下：

```python
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        slow, fast = head, head.next
        # 首先用快慢指针找到链表的中间点
        while fast is not None and fast.next is not None:
            slow, fast = slow.next, fast.next.next
        mid, slow.next = slow.next, None
        left = self.sortList(head)
        right = self.sortList(mid)
        # 在链表中使用归并排序
        h = ListNode(0)
        res = h
        while left is not None and right is not None:
            if left.val < right.val:
                p = left
                left = left.next
            else:
                p = right
                right = right.next
            h.next = p
            h = h.next
        h.next = left if left is not None else right
        return res.next

```



## 0205. 反转链表
> 给定一个链表，返回反转后的链表

- 典中典的链表题，虽然可以直接遍历两次链表先按顺序记录再一个个改变，但是这种方法太弱智了，如果面试里这么写肯定是过不了的。正确的写法应该使用两个指针遍历整个链表，然后每次对next节点进行交换，这样空间复杂度是常数级别的。

```cpp
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if (head == nullptr || head->next == nullptr) {
            return head;
        }
        ListNode *p = nullptr, *q = head;
        // 直接在链表上进行反转
        while (q != nullptr) {
            ListNode* r = q->next;
            q->next = p;
            p = q;
            q = r;
        }
        return p;
    }
};

```
