---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 回溯
  - 模板
  - DFS
cards: []
---

# 回溯刷题模板

> 子集 / 组合 / 排列 三类经典回溯 + 通用模板
> 参考：`references/dsa/2）二.算法/7.回溯/`

---

## 1. 子集

```python
def subsets(nums):
    res, path = [], []

    def backtrack(start):
        res.append(path[:])          # 每个节点都是子集
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1)         # 不重复取，所以 i+1
            path.pop()

    backtrack(0)
    return res
```

**输入**：`[1,2,3]` → **输出**：`[[], [1], [1,2], [1,2,3], [1,3], [2], [2,3], [3]]`

---

## 2. 组合

```python
def combine(n, k):
    res, path = [], []

    def backtrack(start):
        if len(path) == k:
            res.append(path[:])
            return
        for i in range(start, n + 1):
            path.append(i)
            backtrack(i + 1)
            path.pop()

    backtrack(1)
    return res
```

**与子集的唯一区别**：只有当 path 长度达到 k 才记录

---

## 3. 排列

```python
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)

    def backtrack():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                path.append(nums[i])
                backtrack()
                path.pop()
                used[i] = False

    backtrack()
    return res
```

**与子集/组合的关键区别**：每次从 0 开始遍历，用 used[] 避免重复选同一个元素

---

## 4. 通用回溯模板

```python
def backtrack_template(nums):
    res, path = [], []

    def backtrack(start):
        # 满足条件则记录
        if meets_condition(path):
            res.append(path[:])
            # 注意：这里是否 return 取决于是否继续搜索
        for i in range(start, len(nums)):
            # 剪枝：不满足条件的分支跳过
            if not is_valid(nums[i], path):
                continue
            path.append(nums[i])
            backtrack(i + 1)      # 不重复选元素
            # backtrack(i)        # 可重复选元素
            path.pop()

    backtrack(0)
    return res
```

---

## 决策树对比

| 题型 | 参数传递 | 去重方式 | 记录时机 |
|------|---------|---------|---------|
| 子集 | `start` | `i+1` 不重复 | 每个节点 |
| 组合 | `start` | `i+1` 不重复 | 叶子节点（len==k） |
| 排列 | 无 start | `used[]` 标记 | 叶子节点（len==n） |

---

## 核心心法

1. **选择列表**：当前还能选什么 → 用 `start` 或 `used[]` 控制
2. **路径**：已做出的选择 → `path`
3. **结束条件**：什么时候记录 → 到达叶子或满足条件
4. **剪枝**：不合法分支提前跳过 → 排序 + `if i > start and nums[i] == nums[i-1]: continue`

---

## 回顾

- Q: 子集、组合、排列三者的回溯区别？
  A: 子集记录每个节点&start；组合只在 len==k 记录&start；排列没有 start 用 used[] 标记

- Q: 回溯算法的三要素是什么？
  A: 路径（已做的选择）、选择列表（当前可选的）、结束条件（何时记录答案）

- Q: 回溯中的剪枝是什么？
  A: 在递归前判断当前选择是否合法，不合法提前跳过（continue），避免进入无效分支

- Q: 子集为什么每个节点都记录，而排列只记录叶子？
  A: 子集元素顺序无关，[1,2] 和 [2,1] 算同一个，所以每个前缀都是不同子集。排列全排列只关心最终顺序

- Q: Python 回溯用列表传递 path，C++ 一般用什么？
  A: C++ 用 `vector<int>& path` 传引用 + 回溯 `pop_back()`；Python 默认传引用但记录时要 `path[:]` 拷贝副本
