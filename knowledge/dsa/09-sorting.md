---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 排序
  - 模板
  - 快排
  - 归并
  - 堆排
cards: []
---

# 排序算法刷题模板

> 快排 / 归并 / 堆排 三大核心 + 工程排序库对比
> 参考：`references/dsa/2）二.算法/1.排序/`

---

## 1. 快速排序

```python
def quick_sort(nums, left=0, right=None):
    if right is None:
        right = len(nums) - 1
    if left >= right:
        return
    # 分区
    pivot = nums[left]
    i, j = left, right
    while i < j:
        while i < j and nums[j] >= pivot:
            j -= 1
        nums[i] = nums[j]
        while i < j and nums[i] <= pivot:
            i += 1
        nums[j] = nums[i]
    nums[i] = pivot
    # 递归
    quick_sort(nums, left, i - 1)
    quick_sort(nums, i + 1, right)
```

**关键**：挖坑法分区，pivot 取左端点，O(n log n) 平均，O(n²) 最坏

### 快排变形 — 快速选择（找第 k 大）

```python
def find_kth_largest(nums, k):
    def partition(l, r):
        pivot = nums[l]
        i, j = l, r
        while i < j:
            while i < j and nums[j] >= pivot:
                j -= 1
            nums[i] = nums[j]
            while i < j and nums[i] <= pivot:
                i += 1
            nums[j] = nums[i]
        nums[i] = pivot
        return i

    left, right = 0, len(nums) - 1
    target = len(nums) - k  # 第 k 大 → 第 len-k 小的索引
    while left <= right:
        mid = partition(left, right)
        if mid == target:
            return nums[mid]
        elif mid < target:
            left = mid + 1
        else:
            right = mid - 1
```

---

## 2. 归并排序

```python
def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(left, right)

def merge(left, right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res
```

**关键**：分治 + 合并，O(n log n) 稳定，空间 O(n)

### 归并变形 — 数组中的逆序对

```python
def reverse_pairs(nums):
    def merge_sort_count(arr):
        if len(arr) <= 1:
            return arr, 0
        mid = len(arr) // 2
        left, cnt_l = merge_sort_count(arr[:mid])
        right, cnt_r = merge_sort_count(arr[mid:])
        merged, cnt_m = merge_count(left, right)
        return merged, cnt_l + cnt_r + cnt_m

    def merge_count(left, right):
        res, cnt = [], 0
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                res.append(left[i])
                i += 1
            else:
                res.append(right[j])
                cnt += len(left) - i  # 左剩余都比右当前大
                j += 1
        res.extend(left[i:])
        res.extend(right[j:])
        return res, cnt

    return merge_sort_count(nums)[1]
```

---

## 3. 堆排序

```python
def heap_sort(nums):
    n = len(nums)

    def heapify(i, size):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        if left < size and nums[left] > nums[largest]:
            largest = left
        if right < size and nums[right] > nums[largest]:
            largest = right
        if largest != i:
            nums[i], nums[largest] = nums[largest], nums[i]
            heapify(largest, size)

    # 建堆（从最后一个非叶子节点开始）
    for i in range(n // 2 - 1, -1, -1):
        heapify(i, n)

    # 排序
    for i in range(n - 1, 0, -1):
        nums[0], nums[i] = nums[i], nums[0]  # 堆顶 → 末尾
        heapify(0, i)                        # 调整剩余堆
    return nums
```

---

## 4. 工程排序库

```python
# Python
sorted(nums)          # 返回新列表
nums.sort()           # 原地排序
nums.sort(key=lambda x: x[1], reverse=True)  # 按第二元素降序
```

```cpp
// C++: std::sort (混合排序, 通常是内省排序)
#include <algorithm>
std::sort(v.begin(), v.end());                          // 升序
std::sort(v.begin(), v.end(), std::greater<int>());     // 降序
// std::stable_sort — 稳定排序（归并实现）
```

> Python 的 Timsort 是归并+插入的混合算法，最坏 O(n log n) 且对部分有序数据极快。
> C++ `std::sort` 是内省排序（快排+堆排混合），不保证稳定；需要稳定用 `std::stable_sort`。

---

## 复杂度对比

| 算法 | 平均 | 最坏 | 空间 | 稳定 |
|------|------|------|------|------|
| 快排 | O(n log n) | O(n²) | O(log n) | ❌ |
| 归并 | O(n log n) | O(n log n) | O(n) | ✅ |
| 堆排 | O(n log n) | O(n log n) | O(1) | ❌ |
| 冒泡 | O(n²) | O(n²) | O(1) | ✅ |
| 插入 | O(n²) | O(n²) | O(1) | ✅ |

---

## 回顾

- Q: 快排的核心步骤？
  A: 选 pivot → 分区（左小右大）→ 递归排序左右分区

- Q: 归并排序如何计算逆序对？
  A: 合并时，当右半元素小于左半当前元素，说明左半剩余所有元素都大于该右半元素，累加 `len(left) - i`

- Q: Python sorted() 底层用什么算法？
  A: Timsort — 归并+插入混合，对部分有序数据 O(n)，最坏 O(n log n)

- Q: 快排最坏情况什么时候发生？如何改进？
  A: 数组已有序且每次 pivot 选端点 → O(n²)。改进：随机选 pivot / 三数取中

- Q: 堆排的建堆时间复杂度？
  A: O(n)，从最后一个非叶子节点向下调整。排序阶段 n 次出堆 O(n log n)，总计 O(n log n)
