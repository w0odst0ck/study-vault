---
{
  "id": "crawler-Date头是什么时区-072",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "Date 头是什么时区？爬虫时间解析的坑？",
  "a": "UTC（RFC 9110 §5.6.7，比北京慢 8h）；**存储统一 UTC 不转本地，展示才转**（转来转去引入夏令时/时区混乱）；解析用 `email.utils.parsedate_to_datetime()` 别手切字符串",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: Date 头是什么时区？爬虫时间解析的坑？

**A**: UTC（RFC 9110 §5.6.7，比北京慢 8h）；**存储统一 UTC 不转本地，展示才转**（转来转去引入夏令时/时区混乱）；解析用 `email.utils.parsedate_to_datetime()` 别手切字符串
