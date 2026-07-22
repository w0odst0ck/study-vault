---
{
  "id": "dsa-区间DP的典型遍历模-010",
  "domain": "dsa",
  "source": "knowledge/dsa/07-dynamic-programming.md",
  "q": "区间 DP 的典型遍历模式？",
  "a": "外层循环枚举区间长度，内层循环枚举区间起点，dp[i][j] 依赖 dp[i+1][j-1] 等缩小区间",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 区间 DP 的典型遍历模式？

**A**: 外层循环枚举区间长度，内层循环枚举区间起点，dp[i][j] 依赖 dp[i+1][j-1] 等缩小区间
