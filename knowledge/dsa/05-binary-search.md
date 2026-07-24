---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 二分查找
  - 模板
  - 搜索
cards: []
---

# 二分查找刷题模板

> 5 种变体：标准二分 / 第一个等于 / 最后一个等于 / 第一个大于等于 / 最后一个小于等于
> 参考：`references/dsa/2）二.算法/2.搜索/`

---

## 1. 标准二分（查目标）

```python
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
```

**注意**：`mid = left + (right - left) // 2` 防溢出

---

## 2. 查找第一个等于 target 的位置

```python
def find_first_eq(nums, target):
    left, right = 0, len(nums) - 1
    res = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            res = mid
            right = mid - 1  # 向左找第一个
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return res
```

---

## 3. 查找最后一个等于 target 的位置

```python
def find_last_eq(nums, target):
    left, right = 0, len(nums) - 1
    res = -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            res = mid
            left = mid + 1  # 向右找最后一个
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return res
```

**模式识别**：找到后不返回，继续向一侧搜索 → "找第一个向左缩，找最后一个向右缩"

---

## 4. 查找第一个 >= target 的位置

```python
def lower_bound(nums, target):
    left, right = 0, len(nums)  # 注意 right = len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left  # 可能返回 len(nums)
```

**模式识别**：左闭右开区间 [left, right)，最后 left == right 就是答案

---

## 5. 查找最后一个 <= target 的位置

```python
def upper_bound(nums, target):
    left, right = -1, len(nums) - 1  # 注意 left = -1
    while left < right:
        mid = left + (right - left + 1) // 2  # 上取整
        if nums[mid] <= target:
            left = mid
        else:
            right = mid - 1
    return left  # 可能返回 -1
```

---

## 6. 二分答案（值域二分）

当问题答案有单调性时，不用在解空间里线性搜索，而是二分答案后验证。

```python
def binary_search_answer(low, high):
    """在 [low, high] 中找满足条件的最值"""
    while low < high:
        mid = low + (high - low + 1) // 2  # 上取整，找最大值
        if condition(mid):
            low = mid
        else:
            high = mid - 1
    return low
```

**模式识别**：求最大满足条件 / 最小满足条件 → 二分答案范围，check(mid) O(n) 验证

---

## 心法对比

| 变体 | 循环条件 | mid 取整 | 缩区间 | 返回值 |
|------|---------|---------|--------|-------|
| 标准查找 | `left <= right` | 下取整 | `mid ± 1` | 索引 / -1 |
| 第一个等于 | `left <= right` | 下取整 | 找到后 `right = mid - 1` | 索引 / -1 |
| 最后一个等于 | `left <= right` | 下取整 | 找到后 `left = mid + 1` | 索引 / -1 |
| 第一个 >= | `left < right` | 下取整 | `right = mid` | `left` |
| 最后一个 <= | `left < right` | **上取整** | `left = mid` | `left` |

---

## 回顾

- Q: 二分查找的前提条件是什么？
  A: 数据必须有序（单调性），才能通过比较中间值排除一半搜索空间

- Q: 第一个等于和最后一个等于的实现区别？
  A: 找到 target 后，第一个等于向左缩（right = mid - 1），最后一个等于向右缩（left = mid + 1）

- Q: 二分答案的思路是什么？
  A: 不直接搜索答案位置，而是二分答案的值域，用 check(mid) 验证可行性，利用单调性缩小区间

- Q: 边界处理时 `left + (right - left) // 2` 为什么比 `(left + right) // 2` 好？
  A: 防溢出，当 left 和 right 很大时 left+right 可能超过整数上限

- Q: lower_bound 为什么 right 初始化为 len(nums) 而不是 len(nums)-1？
  A: 当所有元素都小于 target 时，答案应为 len(nums)，左闭右开区间允许这个值

- Q: C++ 的 std::lower_bound 和 Python bisect.bisect_left 对应什么？
  A: 都对应「第一个 >= target」的位置。C++ 返回迭代器，Python 返回索引。Python 标准库 `bisect` 模块二分实现比手写更稳
