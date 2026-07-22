---
{
  "id": "programming-FastAPI的a-036",
  "domain": "programming",
  "source": "knowledge/programming/07-fastapi.md",
  "q": "FastAPI 的 `async def` 和 `def` 如何选择？",
  "a": "I/O 密集（async ORM/HTTP 请求）用 `async def`；CPU 密集或同步数据库用 `def`（FastAPI 自动放线程池执行）",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: FastAPI 的 `async def` 和 `def` 如何选择？

**A**: I/O 密集（async ORM/HTTP 请求）用 `async def`；CPU 密集或同步数据库用 `def`（FastAPI 自动放线程池执行）
