---
{
  "id": "crawler-monitor在PH-129",
  "domain": "crawler",
  "source": "knowledge/crawler/18-price-monitoring.md",
  "q": "monitor 在 PH 里的定位？完整数据链路？",
  "a": "- 定位三词诀：**自动下游 · 静默 · 波动才提醒**；消费离线解析产物，纯分析无爬虫；PH 一级功能（与 api/web/cli 平级）\n  - 链路：PH 解析产物（CSV）→ 定时扫描导入（增量）→ 跨批次比价 → 波动检测 → 明显波动写 alerts → 心跳播报；**无常驻进程**（cron 触发）；数据本地不上传",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: monitor 在 PH 里的定位？完整数据链路？

**A**: - 定位三词诀：**自动下游 · 静默 · 波动才提醒**；消费离线解析产物，纯分析无爬虫；PH 一级功能（与 api/web/cli 平级）
  - 链路：PH 解析产物（CSV）→ 定时扫描导入（增量）→ 跨批次比价 → 波动检测 → 明显波动写 alerts → 心跳播报；**无常驻进程**（cron 触发）；数据本地不上传
