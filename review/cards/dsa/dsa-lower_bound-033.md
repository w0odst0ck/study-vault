---
{
  "id": "dsa-lower_bound-033",
  "domain": "dsa",
  "source": "knowledge/dsa/05-binary-search.md",
  "q": "lower_bound 为什么 right 初始化为 len(nums) 而不是 len(nums)-1？",
  "a": "当所有元素都小于 target 时，答案应为 len(nums)，左闭右开区间允许这个值",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: lower_bound 为什么 right 初始化为 len(nums) 而不是 len(nums)-1？

**A**: 当所有元素都小于 target 时，答案应为 len(nums)，左闭右开区间允许这个值
