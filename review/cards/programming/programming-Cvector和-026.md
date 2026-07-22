---
{
  "id": "programming-Cvector和-026",
  "domain": "programming",
  "source": "knowledge/programming/99-cross-language-comparison.md",
  "q": "C++ vector 和 Python list 的扩容差异？",
  "a": "vector 存实际元素，扩容触发 move/copy（迭代器失效）；list 存 PyObject* 指针，扩容只拷贝指针，无迭代器失效问题",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ vector 和 Python list 的扩容差异？

**A**: vector 存实际元素，扩容触发 move/copy（迭代器失效）；list 存 PyObject* 指针，扩容只拷贝指针，无迭代器失效问题
