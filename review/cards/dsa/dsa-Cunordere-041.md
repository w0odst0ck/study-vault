---
{
  "id": "dsa-Cunordere-041",
  "domain": "dsa",
  "source": "knowledge/dsa/04-hash-table.md",
  "q": "C++ unordered_map 和 Python dict 底层实现有什么异同？",
  "a": "都是哈希表。Python dict 用开放地址法（CPython 3.6+ 保持插入顺序），C++ unordered_map 用链地址法，不保证顺序",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: C++ unordered_map 和 Python dict 底层实现有什么异同？

**A**: 都是哈希表。Python dict 用开放地址法（CPython 3.6+ 保持插入顺序），C++ unordered_map 用链地址法，不保证顺序
