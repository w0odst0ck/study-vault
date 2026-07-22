---
{
  "id": "programming-PythonPydan-011",
  "domain": "programming",
  "source": "knowledge/programming/01-pydantic-v2-model-design.md",
  "q": "Python Pydantic 模型和 C++ struct/class 在设计上的核心区别？",
  "a": "Pydantic 模型自带验证/序列化/反序列化（声明式），C++ struct 只是数据容器（需要手写验证）；\n  C++ 类的封装粒度更细（public/protected/private），Python 用 `_`/`__` 约定而非强制",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: Python Pydantic 模型和 C++ struct/class 在设计上的核心区别？

**A**: Pydantic 模型自带验证/序列化/反序列化（声明式），C++ struct 只是数据容器（需要手写验证）；
  C++ 类的封装粒度更细（public/protected/private），Python 用 `_`/`__` 约定而非强制
