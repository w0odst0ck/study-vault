---
{
  "id": "crawler-为什么京东解析器要复用-031",
  "domain": "crawler",
  "source": "knowledge/crawler/08-jd-parser-frontend.md",
  "q": "为什么京东解析器要复用 DOMParser？",
  "a": "每次 parse 7-12MB HTML，三次独立解析性能差。一次解析传 doc 给所有子函数，时间从 3× 降到 1×。jsdom 超 10MB 会崩（Node 端限制，浏览器端正常）",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 为什么京东解析器要复用 DOMParser？

**A**: 每次 parse 7-12MB HTML，三次独立解析性能差。一次解析传 doc 给所有子函数，时间从 3× 降到 1×。jsdom 超 10MB 会崩（Node 端限制，浏览器端正常）
