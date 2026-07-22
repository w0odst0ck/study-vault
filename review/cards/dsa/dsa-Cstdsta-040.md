---
{
  "id": "dsa-Cstdsta-040",
  "domain": "dsa",
  "source": "knowledge/dsa/03-stack-queue.md",
  "q": "C++ std::stack 和 Python list 模拟栈有什么不同？",
  "a": "C++ stack 默认用 deque 做底层容器，禁止遍历只允许 top/push/pop；Python list 模拟栈可任意访问和切片，但大 O 相同",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ std::stack 和 Python list 模拟栈有什么不同？

**A**: C++ stack 默认用 deque 做底层容器，禁止遍历只允许 top/push/pop；Python list 模拟栈可任意访问和切片，但大 O 相同
