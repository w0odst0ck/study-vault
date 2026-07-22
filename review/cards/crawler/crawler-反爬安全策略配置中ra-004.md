---
{
  "id": "crawler-反爬安全策略配置中ra-004",
  "domain": "crawler",
  "source": "knowledge/crawler/01-b2b-platforms-anti-crawl.md",
  "q": "反爬安全策略配置中 rate_limit 的典型值是多少？",
  "a": "典型限速为 10 req/min，配合自适应延时 `request_delay: (0.5, 2.0)` 和指数退避使用。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 反爬安全策略配置中 rate_limit 的典型值是多少？

**A**: 典型限速为 10 req/min，配合自适应延时 `request_delay: (0.5, 2.0)` 和指数退避使用。
