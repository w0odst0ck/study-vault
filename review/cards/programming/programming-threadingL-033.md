---
{
  "id": "programming-threadingL-033",
  "domain": "programming",
  "source": "knowledge/programming/06-python-multitask.md",
  "q": "`threading.Lock` 的 with 语句用法？",
  "a": "`with lock:` 自动 `acquire()`，离开 with 块自动 `release()`，避免忘记释放导致死锁",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: `threading.Lock` 的 with 语句用法？

**A**: `with lock:` 自动 `acquire()`，离开 with 块自动 `release()`，避免忘记释放导致死锁
