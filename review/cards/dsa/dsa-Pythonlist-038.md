---
{
  "id": "dsa-Pythonlist-038",
  "domain": "dsa",
  "source": "knowledge/dsa/01-array-two-pointer-sliding-window.md",
  "q": "Python list、C++ vector、C 数组在内存分配上有什么区别？",
  "a": "Python list 存 PyObject 指针（对象引用），动态扩容 O(n) 摊销 O(1)；C++ vector 连续存储元素，自动倍增扩容；C 数组固定长度栈/堆分配，不自动扩容",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: Python list、C++ vector、C 数组在内存分配上有什么区别？

**A**: Python list 存 PyObject 指针（对象引用），动态扩容 O(n) 摊销 O(1)；C++ vector 连续存储元素，自动倍增扩容；C 数组固定长度栈/堆分配，不自动扩容
