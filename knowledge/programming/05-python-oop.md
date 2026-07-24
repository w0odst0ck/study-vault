---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - Python
  - OOP
  - 封装
  - 继承
  - 多态
  - 魔术方法
cards: []
---

# Python 面向对象编程

> 封装 / 继承 / 多态 + 魔术方法 + 类方法/静态方法
> 来源：旧知识库「编程语言基础/Python/2.面向对象OOP」

---

## 1. 三大特性

| 特性 | 核心 | 关键词 |
|------|------|--------|
| **封装** | 保护数据，隐藏细节 | `__私有`、安全接口 |
| **继承** | 代码复用，减少重复 | `子类(父类)`、`super()` |
| **多态** | 同名方法不同表现 | 重写、统一接口 |

### 封装

```python
class Person:
    def __init__(self, name, age):
        self.name = name      # 公开
        self.__age = age      # 私有（双下划线）
    def get_age(self):
        return self.__age
```

### 继承

```python
class Animal:
    def eat(self):
        print("吃东西")

class Dog(Animal):
    def bark(self):
        print("汪汪")

dog = Dog()
dog.eat()   # 继承得到
dog.bark()  # 自己新增
```

> Python 支持**多重继承**：`class C(A, B)`，注意 MRO（方法解析顺序）使用 C3 线性化。

### 多态

```python
class Cat(Animal):
    def speak(self):
        print("喵")

class Dog(Animal):
    def speak(self):
        print("汪")

def talk(animal):
    animal.speak()  # 同一个接口，不同表现

talk(Cat())  # 喵
talk(Dog())  # 汪
```

> **鸭子类型**：Python 不要求显式继承，只要对象有 `speak` 方法就可以传入 `talk()`。

---

## 2. 属性与方法分类

| 类型 | 第一个参数 | 装饰器 | 访问方式 | 用途 |
|------|-----------|--------|---------|------|
| 实例属性 | — | — | `对象.属性` | 对象专属数据 |
| 类属性 | — | — | `类名.属性` | 所有对象共享 |
| 实例方法 | `self` | 无 | `对象.方法()` | 操作实例属性 |
| 类方法 | `cls` | `@classmethod` | `类名.方法()` | 操作类属性/工厂方法 |
| 静态方法 | 无 | `@staticmethod` | `类名.方法()` | 工具函数，无关属性 |

```python
class Demo:
    class_attr = "共享"       # 类属性

    def __init__(self, val):
        self.inst_attr = val  # 实例属性

    def inst_method(self):    # 实例方法
        return self.inst_attr

    @classmethod
    def cls_method(cls):      # 类方法
        return cls.class_attr

    @staticmethod
    def static_method(x):     # 静态方法
        return x * 2
```

---

## 3. 常用魔术方法

| 方法 | 触发时机 | 用途 |
|------|---------|------|
| `__init__` | `对象()` 创建时 | 初始化实例属性 |
| `__str__` | `print(obj)` / `str(obj)` | 用户友好的描述 |
| `__repr__` | 控制台显示、容器打印 | 开发者可还原的描述 |
| `__call__` | `obj()` 像函数调用 | 让对象可调用 |
| `__enter__`/`__exit__` | `with` 语句 | 上下文管理器 |

```python
class Person:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Person: {self.name}"
    def __repr__(self):
        return f"Person('{self.name}')"
    def __call__(self, n):
        return self.name * n

p = Person("小明")
print(p)    # __str__ → Person: 小明
p           # __repr__ → Person('小明')
p(3)        # __call__ → 小明小明小明
```

---

## 回顾

- Q: Python 封装如何实现私有属性？
  A: 双下划线 `__attr` 触发名称修饰（name mangling），外部不能用 `obj.__attr` 访问

- Q: 类方法（@classmethod）和静态方法（@staticmethod）的区别？
  A: 类方法接收 `cls` 作为第一个参数，可访问类属性/调用其他类方法；静态方法与类无关，就是放在类里的普通函数

- Q: `__str__` 和 `__repr__` 有什么区别？
  A: `__str__` 给用户看（友好），`__repr__` 给开发者看（精确，应能重建对象）。无 `__str__` 时 `__repr__` 会顶替

- Q: `__call__` 让对象具备了什么能力？
  A: 对象可以像函数一样被调用 `obj(args)`，常用于实现函数式接口或类装饰器

- Q: 什么是鸭子类型？
  A: "如果它走路像鸭子、叫起来像鸭子，那它就是鸭子"——Python 不要求显式接口继承，只要对象有对应方法即可传入使用
