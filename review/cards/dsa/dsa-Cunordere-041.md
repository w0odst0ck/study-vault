---
{
  "id": "dsa-Cunordere-041",
  "domain": "dsa",
  "source": "knowledge/dsa/04-hash-table.md",
  "q": "C++ unordered_map 和 Python dict 底层实现有什么异同？",
  "a": "都是哈希表。Python dict 用开放地址法（CPython 3.6+ 保持插入顺序），C++ unordered_map 用链地址法，不保证顺序",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ unordered_map 和 Python dict 底层实现有什么异同？

**A**: 都是哈希表。Python dict 用开放地址法（CPython 3.6+ 保持插入顺序），C++ unordered_map 用链地址法，不保证顺序
