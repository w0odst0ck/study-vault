---
{
  "id": "crawler-本地http_prox-069",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "本地 http_proxy 劫持怎么破？requests 对应什么？",
  "a": "- 坑源 = **环境变量 http_proxy**（requests 默认 trust_env=True 信任它），不是 VPN\n  - 破法：curl `--noproxy '*'` / requests `trust_env=False` 或显式 `proxies={}`",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 本地 http_proxy 劫持怎么破？requests 对应什么？

**A**: - 坑源 = **环境变量 http_proxy**（requests 默认 trust_env=True 信任它），不是 VPN
  - 破法：curl `--noproxy '*'` / requests `trust_env=False` 或显式 `proxies={}`
