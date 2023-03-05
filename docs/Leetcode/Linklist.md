# 数据结构-链表

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
