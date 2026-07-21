---
{
  "id": "crawler-图片提取有哪4级降级-027",
  "domain": "crawler",
  "source": "knowledge/crawler/07-client-side-parser-architecture.md",
  "q": "图片提取有哪 4 级降级策略？",
  "a": "primary（主图）→ secondary（备选）→ thumbnail（缩略图）→ placeholder（占位图），每级失败自动降级。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: 图片提取有哪 4 级降级策略？

**A**: primary（主图）→ secondary（备选）→ thumbnail（缩略图）→ placeholder（占位图），每级失败自动降级。
