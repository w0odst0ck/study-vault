---
{
  "id": "crawler-为什么S1fetch-084",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "为什么 S1 fetcher 必须用 Session？chunked 何时见原始块？",
  "a": "- Session 两理由：① **连接复用省握手**（500 次请求不开 500 次连接）② **cookie 自动回传维持登录态**（不是\"防封\"）\n  - chunked：stream=True 才见原始块（默认透明拼回）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 为什么 S1 fetcher 必须用 Session？chunked 何时见原始块？

**A**: - Session 两理由：① **连接复用省握手**（500 次请求不开 500 次连接）② **cookie 自动回传维持登录态**（不是"防封"）
  - chunked：stream=True 才见原始块（默认透明拼回）
