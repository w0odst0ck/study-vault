---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DSA
  - Python
  - 踩坑
  - 语法
cards: []
---

# Python DSA 刷题常见踩坑

> 来源：LeetCode Hot100 刷题复盘记录
> Python 特有语法坑 / 常见错误模式 / 对比 C++ 差异

---

## 1. 列表操作

### `nums[:] = ...` vs `nums = ...`

```python
# ❌ 新列表，原引用不变
nums = list(set(nums))

# ✅ 原地修改，所有引用都能看到
nums[:] = sorted(set(nums))
```

### `list` 不能作为字典键

```python
# ❌ TypeError: unhashable type: 'list'
group = {}
key = sorted(s)       # sorted() 返回 list
group[key].append(s)

# ✅ 转成 tuple 或 join 成 str
key = tuple(sorted(s))
key = ''.join(sorted(s))
```

### `list.append()` 返回 `None`

```python
# ❌ sorted() 的参数是 None
sorted(nums.append(target))

# ✅ 先 append 再处理
nums.append(target)
nums.sort()
```

---

## 2. 字符串操作

### 字符串不可变

```python
s = "hello"
# ❌ s[0] = 'H'  -> TypeError
# ✅ 重新赋值
s = 'H' + s[1:]
```

### 字符串比较 vs 长度比较

```python
# ❌ 比较的是字典序，不是长度
if substr > longest_substr: ...

# ✅ 用 len()
if len(substr) > len(longest_substr): ...
```

---

## 3. 二分查找边界

二分查找最常见的错误：

```python
# ❌ 死循环！mid 不更新边界
while left <= right:
    mid = (left + right) // 2
    if nums[mid] > target:
        right = mid      # 应改为 right = mid - 1
    else:
        left = mid       # 应改为 left = mid + 1
```

**正确模板**：

```python
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target:
        return mid
    elif nums[mid] < target:
        left = mid + 1
    else:
        right = mid - 1
```

---

## 4. 链表操作

### 遍历后忘记移动指针 → 超时

```python
# ❌ 死循环！忘了移动 list1/list2
while list1 and list2:
    if list1.val <= list2.val:
        current.next = list1
    # 没写 list1 = list1.next

# ✅ 每次比较后都要移动
while list1 and list2:
    if list1.val <= list2.val:
        current.next = list1
        list1 = list1.next
    else:
        current.next = list2
        list2 = list2.next
    current = current.next
```

### `dummy` 节点保底

```python
dummy = ListNode()
current = dummy
# ... 操作 ...
return dummy.next  # 防止头节点为空
```

---

## 5. 栈与括号匹配

```python
# ❌ 只检查栈不为空，没检查栈顶是否匹配
if char in mapping:
    if not stack:
        return False
    # 漏了：if stack[-1] != mapping[char]: return False

# ✅ 完整版本
if char in mapping:
    if not stack or stack[-1] != mapping[char]:
        return False
    stack.pop()
else:
    stack.append(char)
```

---

## 6. 递归与返回值

```python
# ❌ 递归调用结果丢了
def inorder(root):
    lst = []
    inorder(root.left)       # 返回值没收集
    lst.append(root.val)
    inorder(root.right)
    return lst

# ✅ 用 extend 收集子树结果
def inorder(root):
    lst = []
    lst.extend(inorder(root.left))
    lst.append(root.val)
    lst.extend(inorder(root.right))
    return lst
```

---

## 7. Python 特有语法备忘

| 场景 | 正确写法 | 常见错误 |
|------|---------|---------|
| 自增 | `slow += 1` | `slow++`（C 语法） |
| range | `range(n)`, `range(1, n)`, `range(1, n, 2)` | `range(,n)` |
| 类型注解 | `nums: List[int]` | 忘记 import List |
| Optional | `Optional[ListNode]` 表示可能为 None | 漏掉 None 判断 |
| defaultdict | `defaultdict(list)` 避免 KeyError | 手动判断键存在 |
| 类型转换 | `''.join(sorted(s))` | `str(sorted(s))` |

---

## 回顾

- Q: `nums[:] = sorted(set(nums))` 和 `nums = list(set(nums))` 的区别？
  A: 前者原地修改列表（原引用可见），后者创建新列表（原引用不变）。前者保持排序，后者顺序不确定

- Q: 二分查找最常见的 bug 是什么？
  A: 边界更新写成 `right = mid` / `left = mid` 导致死循环。正确是 `right = mid - 1` / `left = mid + 1`，且 mid 用 `left + (right-left)//2` 防溢出

- Q: 链表合并为什么容易超时？
  A: 比较后忘记移动 list1/list2 指针，循环无法推进。每次比较完要 `list1 = list1.next` 或 `list2 = list2.next`

- Q: 列表为什么不能作为字典键？
  A: 列表是可变的（mutable），不可哈希。需要用 `tuple()` 或 `str.join()` 转成不可变类型

- Q: 二叉树递归遍历时为什么用 extend 而不是 append？
  A: 递归返回的是列表，extend 将子列表元素逐个加入主列表，append 会把整个列表当单个元素加入
