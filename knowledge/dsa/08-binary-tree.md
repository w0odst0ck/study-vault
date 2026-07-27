---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 二叉树
  - 模板
  - BFS
  - DFS
cards: []
---

# 二叉树刷题模板

> 遍历、构造、查找、路径 四大类模板
> 参考：`references/dsa/1）一.数据结构/6.树（二叉树）/`

---

## 1. 节点定义

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

> 三语对照：C 用 `struct TreeNode` + 指针；C++ 用 `struct TreeNode` + 智能指针/裸指针

---

## 2. DFS 遍历（递归）

### 前序（根→左→右）

```python
def preorder(root):
    res = []
    def dfs(node):
        if not node:
            return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return res
```

### 中序（左→根→右）

```python
def inorder(root):
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res
```

### 后序（左→右→根）

```python
def postorder(root):
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)
    dfs(root)
    return res
```

**模式识别**：递归三兄弟，只需要调换 `res.append` 的位置

---

## 3. BFS 遍历（层序）

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

**变形**：锯齿形层序（ZigZag）→ 偶数层 `res[-1].reverse()` 或双端队列控制

---

## 4. 二叉树构造

### 前序 + 中序 → 二叉树

```python
def build_tree(preorder, inorder):
    if not preorder or not inorder:
        return None
    root = TreeNode(preorder[0])
    idx = inorder.index(root.val)
    root.left = build_tree(preorder[1:idx+1], inorder[:idx])
    root.right = build_tree(preorder[idx+1:], inorder[idx+1:])
    return root
```

### 中序 + 后序 → 二叉树

```python
def build_tree_in_post(inorder, postorder):
    if not inorder or not postorder:
        return None
    root = TreeNode(postorder[-1])
    idx = inorder.index(root.val)
    root.left = build_tree_in_post(inorder[:idx], postorder[:idx])
    root.right = build_tree_in_post(inorder[idx+1:], postorder[idx:-1])
    return root
```

**模式识别**：前序第一个 / 后序最后一个 = 根节点 → 在中序中定位 → 左右子树递归

---

## 5. 查找与判断

### 查找节点

```python
def find_node(root, target):
    if not root:
        return None
    if root.val == target:
        return root
    return find_node(root.left, target) or find_node(root.right, target)
```

### 判断平衡二叉树

```python
def is_balanced(root):
    def check(node):
        if not node:
            return 0
        left = check(node.left)
        if left == -1:
            return -1
        right = check(node.right)
        if right == -1:
            return -1
        if abs(left - right) > 1:
            return -1
        return max(left, right) + 1
    return check(root) != -1
```

**模式识别**：返回 -1 作为"不合法"哨兵，避免额外全局变量

### 判断 BST

```python
def is_valid_bst(root):
    def check(node, lo, hi):
        if not node:
            return True
        if node.val <= lo or node.val >= hi:
            return False
        return check(node.left, lo, node.val) and check(node.right, node.val, hi)
    return check(root, float('-inf'), float('inf'))
```

---

## 6. 路径与和

### 最大深度

```python
def max_depth(root):
    if not root:
        return 0
    return max(max_depth(root.left), max_depth(root.right)) + 1
```

### 路径总和

```python
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right and root.val == target:
        return True
    return has_path_sum(root.left, target - root.val) or has_path_sum(root.right, target - root.val)
```

---

## 回顾

- Q: 二叉树遍历的递归框架是什么？
  A: 三个位置：前序（先处理根）、中序（中间处理根）、后序（最后处理根）

- Q: 判断平衡二叉树的 -1 哨兵法是什么思路？
  A: 递归返回 -1 表示"已发现非法"，上层收到 -1 直接传播，避免额外状态变量

- Q: 根据前序+中序重建二叉树的步骤？
  A: 前序第一个为根 → 在中序找根索引 → 左子树递归前序[1:idx+1]、中序[:idx] → 右子树递归剩余

- Q: BFS 层序遍历如何区分每一层？
  A: 每层开始时用 `len(q)` 固定当前层大小，循环该次数后开始下一层

- Q: 验证 BST 为什么不能只检查左 < 根 < 右？
  A: 需要全局范围约束（min/max），仅检查局部会漏掉深层违规（如右子树中出现比根小的值）

- Q: C/C++ 中二叉树遍历用递归时需要注意什么？
  A: Python 递归深度默认 ~1000，C++ 递归栈也会有限制。大数据集推荐迭代栈（显式 stack 模拟递归）
