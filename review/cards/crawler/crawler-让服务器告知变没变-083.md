---
{
  "id": "crawler-让服务器告知变没变-083",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "让服务器告知\"变没变\"（不下载全量）怎么做？时间戳方案有什么漏洞？为什么 ETag 补上？",
  "a": "- 时间戳方案 = **Last-Modified/If-Modified-Since 的真实机制**（文无独立设计出协议，神预判）\n  - 漏洞：时间戳是服务器\"声称\"，能撒谎；秒级精度同秒双改漏判；缓存服务器/时钟不准漏更\n  - **ETag = 内容指纹，内容变指纹必变，没法撒谎**——强验证器本质",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 让服务器告知"变没变"（不下载全量）怎么做？时间戳方案有什么漏洞？为什么 ETag 补上？

**A**: - 时间戳方案 = **Last-Modified/If-Modified-Since 的真实机制**（文无独立设计出协议，神预判）
  - 漏洞：时间戳是服务器"声称"，能撒谎；秒级精度同秒双改漏判；缓存服务器/时钟不准漏更
  - **ETag = 内容指纹，内容变指纹必变，没法撒谎**——强验证器本质
