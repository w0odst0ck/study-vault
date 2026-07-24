---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 栈
  - 队列
  - 单调栈
  - 单调队列
  - BFS
cards: []
---

# 栈与队列刷题模板

> 栈：括号匹配 / 单调栈 · 队列：BFS / 单调队列
> 参考：`references/dsa/1）一.数据结构/3.栈/`、`references/dsa/1）一.数据结构/4.队列/`

---

## 1. 栈

### 基本操作（列表模拟）

```python
stack = []
stack.append(1)    # 入栈
stack.append(2)
stack.pop()        # 出栈 → 2
```

### 括号匹配

```python
def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for ch in s:
        if ch in mapping:
            if not stack or stack.pop() != mapping[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
```

**模式识别**：左括号入栈，右括号弹出匹配，最后栈空则合法

### 单调栈 — 下一个更大元素

```python
def next_greater_element(nums):
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            top = stack.pop()
            res[top] = nums[i]
        stack.append(i)
    return res
```

**模式识别**：栈内保持递减 → 遇到更大值时弹出并记录结果

---

## 2. 队列

### 基本操作（deque）

```python
from collections import deque
q = deque()
q.append(1)      # 入队（右端）
q.popleft()      # 出队（左端）
```

### BFS 层序遍历（二叉树）

```python
from collections import deque

def level_order(root):
    if not root:
        return []
    res, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        res.append(level)
    return res
```

---

## 3. 单调队列 — 滑动窗口最大值

```python
from collections import deque

def max_sliding_window(nums, k):
    dq = deque()    # 存索引，保持值递减
    res = []
    for i, num in enumerate(nums):
        # 维护单调递减
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)
        # 移出窗口范围
        if dq[0] <= i - k:
            dq.popleft()
        # 窗口形成后记录
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res
```

**模式识别**：deque 存索引而非值，头部永远是窗口最大值

---

## 心法速查

| 结构 | 本质 | 典型场景 |
|------|------|---------|
| 栈 | 先进后出 | 括号匹配、DFS、撤销操作 |
| 队列 | 先进先出 | BFS、任务队列 |
| 单调栈 | 栈内单调 + O(n) | 下一个更大/更小元素 |
| 单调队列 | deque 内单调 | 滑动窗口最值 |

---

## 回顾

- Q: 括号匹配为什么用栈？
  A: 括号嵌套的闭合顺序是后进先出，栈天然匹配

- Q: 单调栈的核心思路？
  A: 保持栈内元素单调（如递减），遇到破坏单调性的元素就弹出并记录结果，保证每个元素入栈出栈各一次

- Q: 单调队列实现滑动窗口最大值的原理？
  A: deque 存索引，值保持递减。头部是当前窗口最大值，滑动时从头部移除过期索引

- Q: BFS 为什么要用队列？
  A: BFS 需要按层处理，先入先出保证同一层的节点先被访问完再进入下一层

- Q: C++ std::stack 和 Python list 模拟栈有什么不同？
  A: C++ stack 默认用 deque 做底层容器，禁止遍历只允许 top/push/pop；Python list 模拟栈可任意访问和切片，但大 O 相同
