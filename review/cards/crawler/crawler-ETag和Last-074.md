---
{
  "id": "crawler-ETag和Last-074",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "ETag 和 Last-Modified 哪个强？同时存在时带哪个头？",
  "a": "ETag = 内容指纹强验证器（不能撒谎）；Last-Modified = 秒级精度弱验证器（能撒谎）；同时给时只带 **If-None-Match**（服务器 MUST 忽略 If-Modified-Since）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: ETag 和 Last-Modified 哪个强？同时存在时带哪个头？

**A**: ETag = 内容指纹强验证器（不能撒谎）；Last-Modified = 秒级精度弱验证器（能撒谎）；同时给时只带 **If-None-Match**（服务器 MUST 忽略 If-Modified-Since）
