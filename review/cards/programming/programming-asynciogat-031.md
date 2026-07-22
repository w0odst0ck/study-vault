---
{
  "id": "programming-asynciogat-031",
  "domain": "programming",
  "source": "knowledge/programming/06-python-multitask.md",
  "q": "`asyncio.gather()` 的作用？",
  "a": "并发执行多个 awaitable 对象，返回所有结果列表。任一协程异常则全部取消（可用 `return_exceptions=True` 避免）",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: `asyncio.gather()` 的作用？

**A**: 并发执行多个 awaitable 对象，返回所有结果列表。任一协程异常则全部取消（可用 `return_exceptions=True` 避免）
