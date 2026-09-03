---
{
  "id": "crawler-为什么商品ID用正则-092",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "为什么商品 ID 用正则而不是 DOM？价格清洗步骤？",
  "a": "- **分层串联**：DOM 负责定位（哪个 a、哪个 href），正则负责精提取（从 href 抠 `(\\d+)`）——不是二选一\n  - 价格清洗顺序：**先去千分位逗号**（`1,234.50` 的 `\\d+` 只能匹配 \"1\"）→ 再 match 数字 → parseFloat",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 为什么商品 ID 用正则而不是 DOM？价格清洗步骤？

**A**: - **分层串联**：DOM 负责定位（哪个 a、哪个 href），正则负责精提取（从 href 抠 `(\d+)`）——不是二选一
  - 价格清洗顺序：**先去千分位逗号**（`1,234.50` 的 `\d+` 只能匹配 "1"）→ 再 match 数字 → parseFloat
