---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - 编程
  - 跨语言
  - 对比
  - Python
  - C++
  - C
cards: []
---

# C / C++ / Python 三语对比总结

> 融合自三个旧知识库：语法糖（框架/三语参考）+ 编程语言基础（C++ 程序设计 + Python 基础）
> 核心差异速查表

---

## 1. 基础类型与内存

| 维度 | C | C++ | Python |
|------|-----|------|--------|
| 变量声明 | `int x;` | `int x;` / `auto x = 1;` | `x = 1` 动态类型 |
| 数组 | 固定长度 | `std::vector` 动态/静态 | `list` 动态数组 |
| 字符串 | `char*` / `char[]` | `std::string` | `str`（不可变） |
| 内存管理 | 手动 malloc/free | new/delete / RAII | GC（引用计数+分代） |
| 指针/引用 | 指针 | 指针 + 引用 `&` | 无指针（全部对象引用） |

---

## 2. 面向对象

| 特性 | C++ | Python |
|------|-----|--------|
| 封装 | public/protected/private 关键字 | `_` 约定 / `__` 名修饰 |
| 继承 | 单继承+多继承（虚继承解决菱形） | 多继承（C3 MRO） |
| 多态 | 虚函数表（vtable） | 鸭子类型（无虚表） |
| 接口 | 纯虚类（abstract class） | ABC（`@abstractmethod`） |
| 构造/析构 | 构造函数+析构函数（RAII 关键） | `__init__`（无真正析构） |

---

## 3. 容器对比

| 语义 | C++ | Python |
|------|-----|--------|
| 动态数组 | `std::vector` | `list` |
| 链表 | `std::list`（双向） | 无内置（需自定义） |
| 栈 | `std::stack` | `list` 模拟 |
| 队列 | `std::queue` | `collections.deque` |
| 哈希表 | `std::unordered_map` | `dict` |
| 有序字典 | `std::map`（红黑树） | `dict` 3.7+ 插入有序 |
| 集合 | `std::unordered_set` | `set` |

> C++ 容器区分「有序」和「无序」：`map` vs `unordered_map`，`set` vs `unordered_set`。
> Python 统一用 `dict` / `set`，底层都是哈希表。

---

## 4. 关键语言特性

### 装饰器 vs 函数指针 vs Lambda

```python
# Python 装饰器（编译时挂载）
@log("INFO")
def f(): ...
```

```cpp
// C++ 函数指针 / std::function
void logger(std::function<void()> f) {
    std::cout << "BEFORE\n";
    f();
    std::cout << "AFTER\n";
}
// C++ Lambda（临时包装）
logger([]() { /* ... */ });
```

### 生成器 vs 迭代器

```python
# Python yield 自动生成器
def gen():
    for i in range(n):
        yield i
```

```cpp
// C++ 需手写迭代器类或使用 ranges
// C++20 有 std::generator（协程）
```

### 上下文管理器 vs RAII

```python
# Python with 语句
with open("f.txt") as f: ...
```

```cpp
// C++ RAII 构造函数/析构函数自动管理
std::ifstream f("f.txt");
// 出作用域自动关闭（析构）
```

---

## 5. 项目管理对比

| 维度 | Python | C++ |
|------|--------|-----|
| 包管理 | pip / poetry / uv | vcpkg / Conan |
| 构建 | 无（解释执行） | CMake / Make / Bazel |
| 类型检查 | mypy / Pyright（可选） | 编译器强制 |
| 测试 | pytest | Google Test |
| 格式化 | black / ruff | clang-format |
| 依赖文件 | requirements.txt / pyproject.toml | CMakeLists.txt |

---

## 回顾

- Q: Python 的装饰器和 C++ 的函数包装有什么区别？
  A: Python 装饰器在函数定义时（编译时）通过 `@` 语法糖静态挂载；C++ 需在调用处显式包装（Lambda/函数指针），无等效语法糖

- Q: C++ RAII 和 Python with 语句的异同？
  A: 都是资源自动管理。RAII 绑定到变量生命周期（构造获取/析构释放），自动触发；`with` 是显式代码块，依赖 `__enter__`/`__exit__` 协议

- Q: C++ vector 和 Python list 的扩容差异？
  A: vector 存实际元素，扩容触发 move/copy（迭代器失效）；list 存 PyObject* 指针，扩容只拷贝指针，无迭代器失效问题

- Q: C++ 容器为什么需要区分 map 和 unordered_map？
  A: map 基于红黑树 O(log n) 排序存储，支持范围查询；unordered_map 基于哈希表 O(1)，不保证顺序。Python dict 统一用哈希表，3.7+ 额外维护插入顺序

- Q: C++ 和 Python 的包管理关键差异？
  A: Python 包是运行时解析（pip install 即用）；C++ 包需编译（头文件+库文件+链接），vcpkg/Conan 处理源码编译和二进制依赖
