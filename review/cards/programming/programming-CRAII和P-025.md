---
{
  "id": "programming-CRAII和P-025",
  "domain": "programming",
  "source": "knowledge/programming/99-cross-language-comparison.md",
  "q": "C++ RAII 和 Python with 语句的异同？",
  "a": "都是资源自动管理。RAII 绑定到变量生命周期（构造获取/析构释放），自动触发；`with` 是显式代码块，依赖 `__enter__`/`__exit__` 协议",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ RAII 和 Python with 语句的异同？

**A**: 都是资源自动管理。RAII 绑定到变量生命周期（构造获取/析构释放），自动触发；`with` 是显式代码块，依赖 `__enter__`/`__exit__` 协议
