---
{
  "id": "dsa-二分查找最常见的bug-062",
  "domain": "dsa",
  "source": "knowledge/dsa/12-python-dsa-pitfalls.md",
  "q": "二分查找最常见的 bug 是什么？",
  "a": "边界更新写成 `right = mid` / `left = mid` 导致死循环。正确是 `right = mid - 1` / `left = mid + 1`，且 mid 用 `left + (right-left)//2` 防溢出",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: 二分查找最常见的 bug 是什么？

**A**: 边界更新写成 `right = mid` / `left = mid` 导致死循环。正确是 `right = mid - 1` / `left = mid + 1`，且 mid 用 `left + (right-left)//2` 防溢出
