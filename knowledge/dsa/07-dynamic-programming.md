---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - DP
  - 动态规划
  - 模板
cards: []
---

# 动态规划刷题模板

> DP 四类题型模板：线性DP → 区间DP → 背包DP → 树形DP
> 参考：`references/dsa/2）二.算法/3.动态规划/`

---

## 1. 线性 DP

### 一维 DP — 爬楼梯

```python
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    dp = [0] * (n + 1)
    dp[1], dp[2] = 1, 2
    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

**变形**：一次爬 1/2/3 阶 → `dp[i] = dp[i-1] + dp[i-2] + dp[i-3]`

### 二维 DP — 不同路径

```python
def unique_paths(m: int, n: int) -> int:
    dp = [[1] * n for _ in range(m)]
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]
    return dp[m - 1][n - 1]
```

**模式识别**：网格类走法计数 → 左上到右下，只能用向右/向下

---

## 2. 区间 DP — 最长回文子串

```python
def longest_palindrome(s: str) -> str:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    max_len, start = 1, 0
    for i in range(n):
        dp[i][i] = True
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                if length == 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    if length > max_len:
                        max_len, start = length, i
    return s[start:start + max_len]
```

**模式识别**：区间DP = 外层循环长度，内层循环起点，dp[i][j] 依赖 dp[i+1][j-1]（缩小区间）

---

## 3. 背包 DP

### 0-1 背包

```python
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]
```

**空间优化（一维）**：

```python
def knapsack_01_opt(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(capacity, weights[i] - 1, -1):  # 逆序！
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

**模式识别**：0-1 背包内层逆序，完全背包内层正序

> 三语对照：C++ 中同样用 `vector<int> dp(capacity+1, 0)`，内层逆序循环条件相同。
> 参考：`references/dsa/2）二.算法/3.动态规划/`

### 完全背包

```python
def knapsack_complete(weights, values, capacity):
    dp = [0] * (capacity + 1)
    for i in range(len(weights)):
        for w in range(weights[i], capacity + 1):  # 正序！
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]
```

---

## 4. 树形 DP — 最大独立集

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def rob(root: TreeNode) -> int:
    """二叉树上的DP：选或不选当前节点"""
    def dfs(node):
        if not node:
            return [0, 0]  # [不选, 选]
        left = dfs(node.left)
        right = dfs(node.right)
        dp0 = max(left) + max(right)        # 不选当前 → 子节点可选可不选
        dp1 = node.val + left[0] + right[0]  # 选当前 → 子节点只能不选
        return [dp0, dp1]
    return max(dfs(root))
```

**模式识别**：树形DP = 后序遍历 + 每节点返回一个状态数组 → 父节点合并子节点结果

---

## 核心心法

| 要素 | 说明 |
|------|------|
| 状态定义 | `dp[i][j]` 代表什么 → 清晰具体的语义 |
| 转移方程 | 当前状态依赖哪些子状态 → 写出公式 |
| 初始化 | 边界条件（dp[0], dp[0][0]...） |
| 遍历顺序 | 一维/二维/逆序/正序，决定了结果正确性 |
| 空间优化 | 滚动数组：二维→一维，一维→变量 |

---

## 回顾

- Q: 动态规划四步心法是什么？
  A: 定义状态 → 写出转移方程 → 初始化边界 → 确定遍历顺序

- Q: 0-1 背包和完全背包在遍历顺序上的区别？
  A: 0-1 背包内层逆序（保证每个物品只用一次），完全背包内层正序（允许多次使用）

- Q: 树形 DP 的核心写法特征？
  A: 后序遍历，每个节点返回一个状态数组（如 [不选当前, 选当前]），父节点合并子节点结果

- Q: 空间优化中，0-1 背包为什么内层需要逆序？
  A: 逆序遍历 cap 到 w[i]，确保 dp[w] 使用的是上一行的旧值，不会重复使用当前物品

- Q: 区间 DP 的典型遍历模式？
  A: 外层循环枚举区间长度，内层循环枚举区间起点，dp[i][j] 依赖 dp[i+1][j-1] 等缩小区间

- Q: C++ 的 vector 二维数组定义和 Python 列表推导式有什么差异？
  A: Python `[[0]*n for _ in range(m)]`；C++ `vector<vector<int>> dp(m, vector<int>(n, 0))`。注意 Python 不能用 `[[0]*n]*m` 因为会共享引用
