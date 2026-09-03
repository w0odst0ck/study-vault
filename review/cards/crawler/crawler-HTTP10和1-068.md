---
{
  "id": "crawler-HTTP10和1-068",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "HTTP/1.0 和 1.1 对 keep-alive 的默认行为差异？",
  "a": "1.0 默认短连接（`Connection: keep-alive` 才长）；1.1 默认长连接（`Connection: close` 才短）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: HTTP/1.0 和 1.1 对 keep-alive 的默认行为差异？

**A**: 1.0 默认短连接（`Connection: keep-alive` 才长）；1.1 默认长连接（`Connection: close` 才短）
