---
{
  "id": "dsa-Cstdsta-040",
  "domain": "dsa",
  "source": "knowledge/dsa/03-stack-queue.md",
  "q": "C++ std::stack 和 Python list 模拟栈有什么不同？",
  "a": "C++ stack 默认用 deque 做底层容器，禁止遍历只允许 top/push/pop；Python list 模拟栈可任意访问和切片，但大 O 相同",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: C++ std::stack 和 Python list 模拟栈有什么不同？

**A**: C++ stack 默认用 deque 做底层容器，禁止遍历只允许 top/push/pop；Python list 模拟栈可任意访问和切片，但大 O 相同
