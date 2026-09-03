---
{
  "id": "crawler-服务器不给ETag时-076",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "服务器不给 ETag 时增量抓取怎么退路？",
  "a": "① Last-Modified/If-Modified-Since（弱验证，凑合用）② 都没有 → **全量抓取 + 比对内容哈希**（最笨但永远有效）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 服务器不给 ETag 时增量抓取怎么退路？

**A**: ① Last-Modified/If-Modified-Since（弱验证，凑合用）② 都没有 → **全量抓取 + 比对内容哈希**（最笨但永远有效）
