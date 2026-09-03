---
{
  "id": "crawler-429后看哪个头决定等-064",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "429 后看哪个头决定等多久？429 和 503 的处理差异？",
  "a": "- 429 第一优先读 **Retry-After**（秒数/HTTP-date），没有才退避；`time.sleep(int(retry_after))` 前 try/except（服务端可能给坏值）\n  - 语义层：**429 = 服务器没问题（客户端频率问题，冷却即可）vs 503 = 服务端过载（退避试探）**",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 429 后看哪个头决定等多久？429 和 503 的处理差异？

**A**: - 429 第一优先读 **Retry-After**（秒数/HTTP-date），没有才退避；`time.sleep(int(retry_after))` 前 try/except（服务端可能给坏值）
  - 语义层：**429 = 服务器没问题（客户端频率问题，冷却即可）vs 503 = 服务端过载（退避试探）**
