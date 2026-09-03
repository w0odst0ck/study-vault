---
{
  "id": "crawler-Cookie回传的条件-077",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "Cookie 回传的条件是什么？（什么时候带、什么时候不带）",
  "a": "- 四要素：① **Domain** 匹配（含子域，`domain=.example.com` 覆盖 www）② **Path** 前缀命中（`/cart` 的 cookie 不回传给 `/`）③ **Secure** 仅 HTTPS ④ **未过期**（Expires/Max-Age；`Max-Age=0` 主动注销）\n  - 爬虫坑：重定向链跨域丢 cookie",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: Cookie 回传的条件是什么？（什么时候带、什么时候不带）

**A**: - 四要素：① **Domain** 匹配（含子域，`domain=.example.com` 覆盖 www）② **Path** 前缀命中（`/cart` 的 cookie 不回传给 `/`）③ **Secure** 仅 HTTPS ④ **未过期**（Expires/Max-Age；`Max-Age=0` 主动注销）
  - 爬虫坑：重定向链跨域丢 cookie
