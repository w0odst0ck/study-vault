---
{
  "id": "crawler-震坤行的阿里云WAF-003",
  "domain": "crawler",
  "source": "knowledge/crawler/01-b2b-platforms-anti-crawl.md",
  "q": "震坤行的阿里云 WAF 遮罩层如何绕过？",
  "a": "使用 `MutationObserver` 在遮罩元素 `#waf_nc_block` 插入 DOM 之前将其预移除，避免拦截 pointer events。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 震坤行的阿里云 WAF 遮罩层如何绕过？

**A**: 使用 `MutationObserver` 在遮罩元素 `#waf_nc_block` 插入 DOM 之前将其预移除，避免拦截 pointer events。
