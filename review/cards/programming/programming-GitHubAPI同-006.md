---
{
  "id": "programming-GitHubAPI同-006",
  "domain": "programming",
  "source": "knowledge/programming/02-phase-zero-project-startup.md",
  "q": "GitHub API 同步中的三个重要发现是什么？",
  "a": "①`star+json` header 必须带，否则不返回 `starred_at`；② Lists API 返回 404（非个人账号不可用）；③ README 返回 base64 编码，需额外解码。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: GitHub API 同步中的三个重要发现是什么？

**A**: ①`star+json` header 必须带，否则不返回 `starred_at`；② Lists API 返回 404（非个人账号不可用）；③ README 返回 base64 编码，需额外解码。
