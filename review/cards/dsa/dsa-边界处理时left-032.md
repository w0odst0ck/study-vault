---
{
  "id": "dsa-边界处理时left-032",
  "domain": "dsa",
  "source": "knowledge/dsa/05-binary-search.md",
  "q": "边界处理时 `left + (right - left) // 2` 为什么比 `(left + right) // 2` 好？",
  "a": "防溢出，当 left 和 right 很大时 left+right 可能超过整数上限",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 边界处理时 `left + (right - left) // 2` 为什么比 `(left + right) // 2` 好？

**A**: 防溢出，当 left 和 right 很大时 left+right 可能超过整数上限
