---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 数组
  - 字符串
  - 双指针
  - 滑动窗口
  - 模板
cards: []
---

# 数组、双指针、滑动窗口刷题模板

> 四类操作模板：数组遍历 / 双指针 / 滑动窗口 / 前缀和
> 参考：`references/dsa/1）一.数据结构/1.数组与向量/`

---

## 1. 数组 + 字符串基本操作

### 遍历

```python
# 按值
for num in nums:
    ...

# 按索引
for i in range(len(nums)):
    ...
```

### 字符串处理工具箱

```python
ord('A')   # 65 — 字符 → ASCII
chr(65)    # 'A' — ASCII → 字符
s.lower()  # 小写
s.upper()  # 大写
s.split(',')  # 分割 → list
'-'.join(words)  # 合并 → str
s.count('l')    # 计数

from collections import Counter
Counter(nums)  # 频率统计
```

### 排序

```python
sorted(nums)       # 返回新列表
nums.sort()        # 原地排序
nums.sort(key=lambda x: x[1], reverse=True)  # 按第二个元素降序
```

---

## 2. 双指针

### 相向双指针 — 回文判断 / 两数之和

```python
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        elif s < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]
```

**模式识别**：有序数组 + 两数之和 → 相向双指针，O(n) 替代 O(n²) 暴力

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

### 快慢指针 — 原地去重 / 移除元素

```python
def remove_duplicates(nums):
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1
```

**模式识别**：有序数组去重 → 快指针探路，慢指针记录"有效区"边界

---

## 3. 滑动窗口

### 固定窗口大小（如长度 k 的子数组最大和）

```python
def max_sum_fixed_window(nums, k):
    left, right = 0, 0
    window_sum = 0
    max_sum = float('-inf')
    while right < len(nums):
        window_sum += nums[right]
        right += 1
        if right - left == k:
            max_sum = max(max_sum, window_sum)
            window_sum -= nums[left]
            left += 1
    return max_sum
```

### 可变窗口 — 最小覆盖子串

```python
from collections import Counter

def min_window(s, t):
    need = Counter(t)
    window = Counter()
    left = right = 0
    valid = 0
    start, min_len = 0, float('inf')

    while right < len(s):
        c = s[right]
        right += 1
        if c in need:
            window[c] += 1
            if window[c] == need[c]:
                valid += 1

        while valid == len(need):
            if right - left < min_len:
                start = left
                min_len = right - left
            d = s[left]
            left += 1
            if d in need:
                if window[d] == need[d]:
                    valid -= 1
                window[d] -= 1

    return s[start:start + min_len] if min_len != float('inf') else ""
```

**模式识别**：滑动窗口 = 右指针扩张找可行解 + 左指针收缩找最优解

---

## 4. 前缀和

```python
# 构建
nums = [1, 2, 3, 4, 5]
prefix = [0]
for num in nums:
    prefix.append(prefix[-1] + num)

# 区间 [i, j] 的和（左闭右闭）
sub_sum = prefix[j + 1] - prefix[i]
```

**模式识别**：频繁区间求和 → 前缀和 O(1) 查询，空间换时间

---

## 回顾

- Q: 相向双指针适合什么场景？典型题目？
  A: 有序数组 + 两数之和、回文串判断。O(n) 替代 O(n²)

- Q: 快慢指针去重的核心逻辑？
  A: fast 探路，遇到新值就把 slow+1 位置覆盖为新值，slow 始终指向"已处理区"最后一个

- Q: 滑动窗口框架的通用写法？
  A: 右指针扩张（窗口增大）→ 满足条件时左指针收缩（窗口变小）→ 每步更新最优解

- Q: 可变窗口和固定窗口的区别？
  A: 固定窗口在 `right-left == k` 时触发处理+移动左指针；可变窗口在满足条件时持续收缩左指针

- Q: 前缀和解决什么问题？
  A: 频繁的区间求和查询，构建 O(n)，每次查询 O(1)

- Q: Python list、C++ vector、C 数组在内存分配上有什么区别？
  A: Python list 存 PyObject 指针（对象引用），动态扩容 O(n) 摊销 O(1)；C++ vector 连续存储元素，自动倍增扩容；C 数组固定长度栈/堆分配，不自动扩容
