---
{
  "id": "crawler-请求头最小集合是哪几个-062",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "请求头最小集合是哪几个？只留一个留哪个？Host 起什么作用？",
  "a": "- **Host = HTTP/1.1 唯一必须请求头**（RFC 9112 §3.2）——虚拟主机路由：一个 IP 挂多域名，服务器靠 Host 区分；**IP 是 TCP 层的事**，不在报文里\n  - 爬虫最小实用三件套：Host + UA（礼貌+反爬）+ If-None-Match（增量前提）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 请求头最小集合是哪几个？只留一个留哪个？Host 起什么作用？

**A**: - **Host = HTTP/1.1 唯一必须请求头**（RFC 9112 §3.2）——虚拟主机路由：一个 IP 挂多域名，服务器靠 Host 区分；**IP 是 TCP 层的事**，不在报文里
  - 爬虫最小实用三件套：Host + UA（礼貌+反爬）+ If-None-Match（增量前提）
