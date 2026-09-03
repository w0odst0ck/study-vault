---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - Python
  - 高级特性
  - 装饰器
  - 生成器
  - 上下文管理器
  - 闭包
cards: []
---

# Python 高级特性

> 装饰器 / 生成器 / 上下文管理器 / 闭包 — Python 面试必考四件套
> 来源：旧知识库「编程语言基础/Python/3.高级特性」

---

## 1. 装饰器

### 核心口诀

```
外层接收函数，内层添加功能；
遇见参数用 args kwargs；
想带参数套三层；
记得加上 wraps 保留元信息。
```

### 标准模板

```python
from functools import wraps

def decorator(func):
    @wraps(func)          # 保留原函数元信息（必写）
    def wrapper(*args, **kwargs):
        # 原函数执行前
        res = func(*args, **kwargs)
        # 原函数执行后
        return res
    return wrapper
```

### 带参数的装饰器

```python
def log(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] 调用 {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log("INFO")
def test(): ...
```

**模式识别**：装饰器三嵌套（接收参数→接收函数→执行逻辑），`@wraps` 一定要写

---

## 2. 生成器与迭代器

| 类型 | 写法 | 内存 | 核心方法 |
|------|------|------|---------|
| 迭代器 | `iter()` / 自定义类 | 省 | `next()` |
| 生成器 | 函数 + `yield` | **极省** | `yield`/`next()` |

```python
def count_up_to(n):
    i = 0
    while i < n:
        yield i   # 暂停并返回值
        i += 1    # 下次 next() 从这里继续

for x in count_up_to(5):
    print(x)
```

**模式识别**：`yield` 把函数变成生成器→用到才生成→适合大数据流

---

## 3. 闭包

```python
def make_counter():
    count = 0
    def add():
        nonlocal count
        count += 1
        return count
    return add

c = make_counter()
c()  # 1
c()  # 2  # count 被保留，不会重置
```

**核心**：内部函数引用外部函数的变量 → 外部函数退出后变量不销毁

**用途**：装饰器的基础、数据封装、计数器

> 三语对照：C++ 用 lambda 捕获（`[=]` 按值/`[&]` 按引用）实现类似闭包效果，
> 但无 `nonlocal` 等效机制，捕获的变量生命周期需手动管理。

---

## 4. 上下文管理器

### with 语句

```python
with open("file.txt", "r") as f:
    data = f.read()
# 自动关闭，永不漏关
```

**核心价值**：自动分配/释放资源，替代 `try/finally`

### 自定义 - 类实现

```python
class MyResource:
    def __enter__(self):
        print("资源已开启")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("资源已自动关闭")
```

### 自定义 - 生成器简化（推荐）

```python
from contextlib import contextmanager

@contextmanager
def my_open():
    print("开启资源")
    yield          # 执行 with 块内代码
    print("关闭资源")
```

---

## 习语速查

| 特性 | 一句话 | 关键词 |
|------|--------|--------|
| 装饰器 | 不修改原函数，动态添加功能 | `@wraps`、`*args, **kwargs` |
| 生成器 | 用到才生成，极省内存 | `yield`、延迟计算 |
| 闭包 | 外函数退出，内变量不销毁 | `nonlocal`、函数工厂 |
| 上下文管理器 | 自动分配/释放，安全简洁 | `__enter__`/`__exit__`、`@contextmanager` |

---

## 回顾

- Q: 装饰器标准模板的结构？
  A: `def decorator(func): @wraps(func); def wrapper(*args,**kwargs): ... ; return wrapper`

- Q: 生成器和普通函数的区别？
  A: 生成器函数用 `yield` 返回值，调用时返回生成器对象，执行到 yield 暂停，下次 next() 继续

- Q: 闭包的三要素？
  A: 函数嵌套、内部函数引用外部变量、外部函数返回内部函数

- Q: 为什么 `@wraps(func)` 很重要？
  A: 保留原函数的 `__name__`、`__doc__` 等元信息，否则被 wrapper 覆盖导致调试困难

- Q: `@contextmanager` 装饰器的 yield 做了什么？
  A: yield 分割了上下文：yield 前是 `__enter__` 逻辑，yield 后是 `__exit__` 逻辑
