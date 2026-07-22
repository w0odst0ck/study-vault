---
{
  "id": "programming-为什么wraps-017",
  "domain": "programming",
  "source": "knowledge/programming/04-python-advanced.md",
  "q": "为什么 `@wraps(func)` 很重要？",
  "a": "保留原函数的 `__name__`、`__doc__` 等元信息，否则被 wrapper 覆盖导致调试困难",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 为什么 `@wraps(func)` 很重要？

**A**: 保留原函数的 `__name__`、`__doc__` 等元信息，否则被 wrapper 覆盖导致调试困难
