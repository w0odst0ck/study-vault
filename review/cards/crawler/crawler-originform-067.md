---
{
  "id": "crawler-originform-067",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "origin-form 和 absolute-form 的区别？分别发给谁？",
  "a": "origin-form `GET / HTTP/1.1` → 源服务器；absolute-form `GET http://host/path HTTP/1.1` → 正向代理（RFC 9112 §3.2.2/3.2.3）；同一 curl 两种形态取决于发给谁",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: origin-form 和 absolute-form 的区别？分别发给谁？

**A**: origin-form `GET / HTTP/1.1` → 源服务器；absolute-form `GET http://host/path HTTP/1.1` → 正向代理（RFC 9112 §3.2.2/3.2.3）；同一 curl 两种形态取决于发给谁
