---
{
  "id": "programming-contextman-018",
  "domain": "programming",
  "source": "knowledge/programming/04-python-advanced.md",
  "q": "`@contextmanager` 装饰器的 yield 做了什么？",
  "a": "yield 分割了上下文：yield 前是 `__enter__` 逻辑，yield 后是 `__exit__` 逻辑",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: `@contextmanager` 装饰器的 yield 做了什么？

**A**: yield 分割了上下文：yield 前是 `__enter__` 逻辑，yield 后是 `__exit__` 逻辑
