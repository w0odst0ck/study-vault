---
{
  "id": "crawler-爬虫架构中新增一个数据源-012",
  "domain": "crawler",
  "source": "knowledge/crawler/03-national-standard-collection.md",
  "q": "爬虫架构中新增一个数据源需要改哪些代码？",
  "a": "只需写适配器类（继承 `BaseCollector`）+ 在 `standards_config.ini` 注册配置，引擎代码零修改。",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-19",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-20",
  "reviews": 1
}
---

**Q**: 爬虫架构中新增一个数据源需要改哪些代码？

**A**: 只需写适配器类（继承 `BaseCollector`）+ 在 `standards_config.ini` 注册配置，引擎代码零修改。
