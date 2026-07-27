---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 链表
  - 模板
  - 快慢指针
cards: []
---

# 链表刷题模板

> 7 类核心操作：定义 → 遍历 → 创建 → 反转 → 合并 → 环检测 → 删除
> 参考：`references/dsa/1）一.数据结构/2.链表/`

---

## 1. 节点定义

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

> 三语对照：C 用 `typedef struct ListNode {...} ListNode;` + `->` 访问指针。
> C++ 用模板 `template<typename T> struct ListNode { T data; ListNode* next; };`

---

## 2. 遍历

```python
def traverse(head):
    cur = head
    while cur:
        print(cur.val)
        cur = cur.next
```

---

## 3. 创建链表（列表 → 链表）

```python
def create_linked_list(lst):
    if not lst:
        return None
    head = ListNode(lst[0])
    cur = head
    for num in lst[1:]:
        cur.next = ListNode(num)
        cur = cur.next
    return head
```

---

## 4. 反转链表

### 迭代法

```python
def reverse_list_iter(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next
        cur.next = prev
        prev, cur = cur, nxt
    return prev
```

### 递归法

```python
def reverse_list_recursive(head):
    if not head or not head.next:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

**模式识别**：迭代三指针（prev/cur/nxt），递归想成"已经反好了后面，只剩当前节点"

---

## 5. 合并两个有序链表

```python
def merge_two_lists(l1, l2):
    dummy = ListNode()
    cur = dummy
    while l1 and l2:
        if l1.val < l2.val:
            cur.next = l1
            l1 = l1.next
        else:
            cur.next = l2
            l2 = l2.next
        cur = cur.next
    cur.next = l1 or l2
    return dummy.next
```

---

## 6. 环形链表检测与入口

```python
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return slow  # 相遇点
    return None

def detect_cycle_start(head):
    meet = has_cycle(head)
    if not meet:
        return None
    ptr = head
    while ptr != meet:
        ptr = ptr.next
        meet = meet.next
    return ptr
```

**模式识别**：快慢指针相遇 → 从头到入口距离 = 相遇点到入口距离

---

## 7. 删除节点

### 删除当前节点（只给节点引用）

```python
def delete_node(node):
    node.val = node.next.val
    node.next = node.next.next
```

### 删除指定值的所有节点

```python
def delete_nodes_with_value(head, val):
    dummy = ListNode(next=head)
    cur = dummy
    while cur.next:
        if cur.next.val == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next
```

**模式识别**：链表删除 → 用 dummy 节点避免头节点特殊处理

---

## 关键心法

| 技巧 | 场景 |
|------|------|
| `dummy` 哨兵节点 | 任何需要修改头节点的操作（删除/合并） |
| 快慢指针 | 找中点、环检测、倒数第 k 个节点 |
| prev/cur/nxt 三指针 | 反转、区间反转 |

---

## 回顾

- Q: 反转链表的迭代法（prev/cur/nxt）是什么？
  A: prev 指向已反转部分头，cur 指向当前待反转节点，nxt 保存后续。每次 cur.next = prev 后整体前移。

- Q: 链表操作中 dummy 节点的作用？
  A: 作为哨兵头节点，使头节点的插入/删除无需特判，简化代码

- Q: 环形链表入口如何推导？
  A: 快慢指针相遇 → 一个指针从头走，另一个从相遇点走，相遇处即为入口

- Q: 合并有序链表的时间/空间复杂度？
  A: O(n+m) 时间，O(1) 空间（dummy 不算），只改变指针不创建新节点

- Q: 链表递归反转的思路？
  A: 假设后面已经反转好了，当前 head.next 指向了反转后的尾节点，让 head.next.next = head 完成局部反转

- Q: C 和 C++ 链表节点定义有什么区别？
  A: C 用 `struct ListNode { int val; struct ListNode* next; }` + typedef；C++ 用 template 泛型，构造函数初始化，可选智能指针
