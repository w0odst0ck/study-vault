---
{
  "id": "dsa-numss-061",
  "domain": "dsa",
  "source": "knowledge/dsa/12-python-dsa-pitfalls.md",
  "q": "`nums[:] = sorted(set(nums))` 和 `nums = list(set(nums))` 的区别？",
  "a": "前者原地修改列表（原引用可见），后者创建新列表（原引用不变）。前者保持排序，后者顺序不确定",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: `nums[:] = sorted(set(nums))` 和 `nums = list(set(nums))` 的区别？

**A**: 前者原地修改列表（原引用可见），后者创建新列表（原引用不变）。前者保持排序，后者顺序不确定
