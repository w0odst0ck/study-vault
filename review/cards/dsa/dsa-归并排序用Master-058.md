---
{
  "id": "dsa-归并排序用Master-058",
  "domain": "dsa",
  "source": "knowledge/dsa/11-complexity-analysis.md",
  "q": "归并排序用 Master Theorem 怎么算？",
  "a": "T(n) = 2T(n/2) + O(n) → a=2, b=2, f(n)=n → log_2(2)=1 → 情况2 → Θ(n log n)",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 归并排序用 Master Theorem 怎么算？

**A**: T(n) = 2T(n/2) + O(n) → a=2, b=2, f(n)=n → log_2(2)=1 → 情况2 → Θ(n log n)
