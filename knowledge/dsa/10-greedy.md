---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 贪心
  - 模板
cards: []
---

# 贪心算法刷题模板

> 贪心策略四步法 + 5 类经典题型
> 参考：`references/dsa/2）二.算法/4.贪心/`

---

## 贪心四步法

| 步骤 | 说明 |
|------|------|
| 1. **分析问题** | 确定是否有贪心选择性质（局部最优→全局最优）和最优子结构 |
| 2. **选择策略** | 每一步选当前最优：结束最早 / 差值最大 / 收益最高 |
| 3. **数据结构** | 排序 / 优先队列 / 双指针 — 让"选最优"高效 |
| 4. **迭代过程** | 循环选择 → 更新状态 → 继续下一步 |

---

## 经典题型

### 1. 区间调度 — 选最多不重叠区间

```python
def max_non_overlapping(intervals):
    intervals.sort(key=lambda x: x[1])  # 按结束时间排序
    count, end = 0, float('-inf')
    for s, e in intervals:
        if s >= end:
            count += 1
            end = e
    return count
```

**策略**：每次选**结束最早**的，为后面留出最大空间

### 2. 跳跃游戏 — 能否到达末尾

```python
def can_jump(nums):
    max_reach = 0
    for i in range(len(nums)):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + nums[i])
    return True
```

**策略**：维护当前能到达的最远位置，每一步贪心更新

### 3. 分发饼干 — 满足最多孩子

```python
def find_content_children(g, s):
    g.sort()          # 孩子胃口
    s.sort()          # 饼干尺寸
    i = j = 0
    while i < len(g) and j < len(s):
        if s[j] >= g[i]:
            i += 1   # 满足一个孩子
        j += 1
    return i
```

**策略**：最小饼干喂最小胃口的孩子，不浪费

### 4. 加油站 — 环形能走一圈的起点

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    start, tank = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:       # 从 start 到 i 不可行
            start = i + 1  # 尝试起点 i+1
            tank = 0
    return start
```

**策略**：总油量≥总消耗一定有解；累积油量变负则之前所有起点都不可能

### 5. 贪心 + 优先队列 — 合并 K 个有序链表

```python
import heapq

def merge_k_lists(lists):
    dummy = ListNode()
    cur = dummy
    heap = [(l.val, i, l) for i, l in enumerate(lists) if l]
    heapq.heapify(heap)
    while heap:
        val, i, node = heapq.heappop(heap)
        cur.next = node
        cur = cur.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))
    return dummy.next
```

---

## 贪心 vs DP

| | 贪心 | DP |
|--|------|----|
| 决策方式 | 一步到位，不回头 | 多阶段决策，选最优子结构 |
| 证明 | 需要证明局部最优→全局最优 | 转移方程保证全局最优 |
| 效率 | O(n) / O(n log n) | O(n²) / O(n×m) |
| 典型 | 区间调度、Huffman 编码 | 背包、编辑距离 |

**模式识别**：贪心 = 排序/优先队列 + 线性扫描；如果不能一步到位 → 考虑 DP

---

## 回顾

- Q: 区间调度为什么按结束时间排序？
  A: 结束最早 = 给后面留的时间最多，贪心保证全局最优

- Q: 跳跃游戏如何判断能否到达末尾？
  A: 遍历每个位置，维护 max_reach，如果 i > max_reach 说明中间断了

- Q: 分发饼干为什么先排序再匹配？
  A: 排序后可以用双指针 O(n log n) 实现最小浪费匹配

- Q: 加油站问题中累积油量变负后为什么跳过之前所有起点？
  A: 如果 [start, i] 累积为负，说明中间任何起点到 i 都会更早变负，不如直接试 i+1

- Q: 贪心和 DP 怎么区分？
  A: 贪心一步到位不回头（局部决策→全局最优）；DP 多阶段保留所有可能（填表求最优）
