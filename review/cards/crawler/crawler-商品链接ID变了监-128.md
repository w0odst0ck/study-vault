---
{
  "id": "crawler-商品链接ID变了监-128",
  "domain": "crawler",
  "source": "knowledge/crawler/18-price-monitoring.md",
  "q": "商品链接（ID）变了，监控为什么静默？怎么安全合并新旧商品？",
  "a": "- ID 变 = 新商品（新 products 行）→ 无历史基线 → **永远卡学习期** → 静默\n  - 修复三步链：title 归一化 **detect**（小写/去空白/去全角/去首尾标点）→ **只报告不自动合并**（防误并串基线）→ 人工确认合并（多维度匹配：platform+title+店铺名，标注来历可追溯）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 商品链接（ID）变了，监控为什么静默？怎么安全合并新旧商品？

**A**: - ID 变 = 新商品（新 products 行）→ 无历史基线 → **永远卡学习期** → 静默
  - 修复三步链：title 归一化 **detect**（小写/去空白/去全角/去首尾标点）→ **只报告不自动合并**（防误并串基线）→ 人工确认合并（多维度匹配：platform+title+店铺名，标注来历可追溯）
