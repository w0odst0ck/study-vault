---
{
  "id": "crawler-304为什么没有bo-061",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "304 为什么没有 body？客户端靠什么拿到内容？304 是重定向吗？",
  "a": "- 304 = \"没变\"信号（3xx 无 body 无 Location，RFC 9110 §15.4.5）；服务端不发 body = 内容没变客户端已有，发了浪费带宽\n  - 客户端靠**本地缓存**（上次 200 存的 body）+ 验证器（ETag/Last-Modified）确认后直接使用\n  - **301 = 指路牌（搬家带 Location）；304 = 盖章（没变照用）**；304 对应增量抓取 = 跳过解析用旧快照",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 304 为什么没有 body？客户端靠什么拿到内容？304 是重定向吗？

**A**: - 304 = "没变"信号（3xx 无 body 无 Location，RFC 9110 §15.4.5）；服务端不发 body = 内容没变客户端已有，发了浪费带宽
  - 客户端靠**本地缓存**（上次 200 存的 body）+ 验证器（ETag/Last-Modified）确认后直接使用
  - **301 = 指路牌（搬家带 Location）；304 = 盖章（没变照用）**；304 对应增量抓取 = 跳过解析用旧快照
