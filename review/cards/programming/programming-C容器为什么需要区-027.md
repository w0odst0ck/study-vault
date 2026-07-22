---
{
  "id": "programming-C容器为什么需要区-027",
  "domain": "programming",
  "source": "knowledge/programming/99-cross-language-comparison.md",
  "q": "C++ 容器为什么需要区分 map 和 unordered_map？",
  "a": "map 基于红黑树 O(log n) 排序存储，支持范围查询；unordered_map 基于哈希表 O(1)，不保证顺序。Python dict 统一用哈希表，3.7+ 额外维护插入顺序",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ 容器为什么需要区分 map 和 unordered_map？

**A**: map 基于红黑树 O(log n) 排序存储，支持范围查询；unordered_map 基于哈希表 O(1)，不保证顺序。Python dict 统一用哈希表，3.7+ 额外维护插入顺序
