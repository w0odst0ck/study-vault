---
{
  "id": "crawler-keepalive情-063",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "keep-alive 情况下服务端关闭连接的理由？哪个是服务器\"明说\"？爬虫要手动处理吗？",
  "a": "- 记忆锚「**旧/说/晾/挤**」：① 协议旧（HTTP/1.0 默认短连接）② 明说（`Connection: close` 头）③ 空闲超时（晾着不说话）④ 满员（连接数上限关最老）\n  - 爬虫无感：**透明重连**（连接池自动重建），不用手动处理",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: keep-alive 情况下服务端关闭连接的理由？哪个是服务器"明说"？爬虫要手动处理吗？

**A**: - 记忆锚「**旧/说/晾/挤**」：① 协议旧（HTTP/1.0 默认短连接）② 明说（`Connection: close` 头）③ 空闲超时（晾着不说话）④ 满员（连接数上限关最老）
  - 爬虫无感：**透明重连**（连接池自动重建），不用手动处理
