---
{
  "id": "programming-GIL是什么对多线程-029",
  "domain": "programming",
  "source": "knowledge/programming/06-python-multitask.md",
  "q": "GIL 是什么？对多线程有什么影响？",
  "a": "Global Interpreter Lock，同一时刻只有一个线程执行 Python 字节码。CPU 密集任务多线程反而慢，I/O 密集任务多线程可用（I/O 等待时释放 GIL）",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: GIL 是什么？对多线程有什么影响？

**A**: Global Interpreter Lock，同一时刻只有一个线程执行 Python 字节码。CPU 密集任务多线程反而慢，I/O 密集任务多线程可用（I/O 等待时释放 GIL）
