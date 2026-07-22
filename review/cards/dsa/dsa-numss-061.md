---
{
  "id": "dsa-numss-061",
  "domain": "dsa",
  "source": "knowledge/dsa/12-python-dsa-pitfalls.md",
  "q": "`nums[:] = sorted(set(nums))` 和 `nums = list(set(nums))` 的区别？",
  "a": "前者原地修改列表（原引用可见），后者创建新列表（原引用不变）。前者保持排序，后者顺序不确定",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: `nums[:] = sorted(set(nums))` 和 `nums = list(set(nums))` 的区别？

**A**: 前者原地修改列表（原引用可见），后者创建新列表（原引用不变）。前者保持排序，后者顺序不确定
