---
{
  "id": "crawler-跨天去重用什么方法清理-019",
  "domain": "crawler",
  "source": "knowledge/crawler/05-multi-source-intel-collection.md",
  "q": "跨天去重用什么方法？清理策略是什么？",
  "a": "MD5 hash 持久化去重，30 天过期自动清理。23 条源数据第二次采集 0 条，全被去重拦住。\n```",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 跨天去重用什么方法？清理策略是什么？

**A**: MD5 hash 持久化去重，30 天过期自动清理。23 条源数据第二次采集 0 条，全被去重拦住。
```
