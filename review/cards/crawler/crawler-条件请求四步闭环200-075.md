---
{
  "id": "crawler-条件请求四步闭环200-075",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "条件请求四步闭环（200+ETag → 304 → 变化 → 200+新ETag）对应增量抓取的什么？",
  "a": "- 四步：① 首次 200 + body + ETag → **存** ② 轮询带 `If-None-Match: <旧ETag>` ③a 没变 → 304 → 用旧快照跳过解析 ③b 变了 → 200 + 新 body + **新 ETag** ④ **更新存储的 ETag**\n  - 不更新 → 永远 304（错过新内容）或永远 200（白请求）——S1 fetcher 核心",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 条件请求四步闭环（200+ETag → 304 → 变化 → 200+新ETag）对应增量抓取的什么？

**A**: - 四步：① 首次 200 + body + ETag → **存** ② 轮询带 `If-None-Match: <旧ETag>` ③a 没变 → 304 → 用旧快照跳过解析 ③b 变了 → 200 + 新 body + **新 ETag** ④ **更新存储的 ETag**
  - 不更新 → 永远 304（错过新内容）或永远 200（白请求）——S1 fetcher 核心
