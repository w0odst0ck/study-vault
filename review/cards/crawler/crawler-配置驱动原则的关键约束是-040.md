---
{
  "id": "crawler-配置驱动原则的关键约束是-040",
  "domain": "crawler",
  "source": "knowledge/crawler/09-multi-source-collection-pipeline.md",
  "q": "配置驱动原则的关键约束是什么？",
  "a": "config.toml 是唯一数据源配置，代码不做硬编码。新增源只改 toml + 写适配器（如有新协议），采集器 CLI 只读 config 不关心具体来源。",
  "created": "2026-07-23",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-23",
  "reviews": 0
}
---

**Q**: 配置驱动原则的关键约束是什么？

**A**: config.toml 是唯一数据源配置，代码不做硬编码。新增源只改 toml + 写适配器（如有新协议），采集器 CLI 只读 config 不关心具体来源。
