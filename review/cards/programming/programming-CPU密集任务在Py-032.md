---
{
  "id": "programming-CPU密集任务在Py-032",
  "domain": "programming",
  "source": "knowledge/programming/06-python-multitask.md",
  "q": "CPU 密集任务在 Python 中应该用什么？",
  "a": "`multiprocessing.Pool` — 多进程绕开 GIL，利用多核并行",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: CPU 密集任务在 Python 中应该用什么？

**A**: `multiprocessing.Pool` — 多进程绕开 GIL，利用多核并行
