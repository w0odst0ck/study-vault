---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - 哈希表
  - 模板
  - Counter
  - 两数之和
cards: []
---

# 哈希表刷题模板

> 四大场景：计数 / 查找 / 映射 / 分组
> 参考：`references/dsa/1）一.数据结构/5.哈希表/`

---

## 1. 计数

### 手动字典

```python
def count_elements(nums):
    d = {}
    for num in nums:
        d[num] = d.get(num, 0) + 1
    return d
```

### Counter

```python
from collections import Counter
c = Counter(nums)
# c.most_common(1)  → [(val, count)]
```

**模式识别**：频率统计 → 无脑 Counter，需要自定义计数逻辑时用 `defaultdict(int)`

---

## 2. 查找 — 两数之和

```python
def two_sum(nums, target):
    d = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in d:
            return [d[complement], i]
        d[num] = i
    return []
```

**核心思路**：遍历时把"需要配对"的信息存进哈希表。键 = 值，值 = 索引 → O(n)

---

## 3. 去重检查

```python
def contains_duplicate(nums):
    return len(set(nums)) != len(nums)
```

或：

```python
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
```

---

## 4. 映射 — 字符替换

```python
def char_mapping(s):
    """返回字符到序号的映射"""
    return {ch: i for i, ch in enumerate(dict.fromkeys(s))}
```

---

## 5. 分组 — 异位词分组

```python
from collections import defaultdict

def group_anagrams(strs):
    groups = defaultdict(list)
    for s in strs:
        key = ''.join(sorted(s))
        groups[key].append(s)
    return list(groups.values())
```

**模式识别**：需要按某种特征分组 → 特征作为哈希键，组内元素作为值列表

---

## 技巧速查

| 场景 | 方案 | 键 | 值 |
|------|------|----|----|
| 统计频率 | Counter | 元素 | 出现次数 |
| 快速查找 | dict | 查找条件 | 索引/对象 |
| 缓存 | dict/lru_cache | 输入 | 输出 |
| 分组 | defaultdict(list) | 分组特征 | 同组元素列表 |

---

## 回顾

- Q: 两数之和的哈希解法为什么是 O(n)？
  A: 一次遍历，每个元素检查 complement 是否在哈希表中，哈希查找 O(1)

- Q: Counter 和手动 dict 计数的区别？
  A: Counter 是 dict 子类，内置 most_common() 排序，适合快速频率统计；手动 dict 适合需要额外逻辑的场景

- Q: 异位词分组为什么要排序作为 key？
  A: 异位词排序后相同，排序字符串是稳定且唯一的组标识

- Q: set 去重的原理？
  A: 哈希存已见元素，遇到重复时 O(1) 检测到

- Q: C++ unordered_map 和 Python dict 底层实现有什么异同？
  A: 都是哈希表。Python dict 用开放地址法（CPython 3.6+ 保持插入顺序），C++ unordered_map 用链地址法，不保证顺序
