---
{
  "id": "crawler-请求响应报文哪几部分对-081",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "请求/响应报文哪几部分对称？空行起什么作用？你的 IP 在报文里吗？",
  "a": "- 四段对称：**首行 + 头 + 空行 + body**（请求首行=请求行，响应首行=状态行）\n  - **空行 = 分界线**（头部到此结束，后面是 body）——不是占位\n  - IP 不在 HTTP 报文里，在 TCP/IP 层（curl `*` 行=连接层，`>`/`<`=报文）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 请求/响应报文哪几部分对称？空行起什么作用？你的 IP 在报文里吗？

**A**: - 四段对称：**首行 + 头 + 空行 + body**（请求首行=请求行，响应首行=状态行）
  - **空行 = 分界线**（头部到此结束，后面是 body）——不是占位
  - IP 不在 HTTP 报文里，在 TCP/IP 层（curl `*` 行=连接层，`>`/`<`=报文）
