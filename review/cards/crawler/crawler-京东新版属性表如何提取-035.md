---
{
  "id": "crawler-京东新版属性表如何提取-035",
  "domain": "crawler",
  "source": "knowledge/crawler/08-jd-parser-frontend.md",
  "q": "京东新版属性表如何提取？",
  "a": "`<div class=attrs>` 存在于渲染 DOM。新版通过 unquoted attrs 正则匹配提取，非旧版 CSS class 匹配",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-17",
  "interval": 1,
  "ease": 2.5,
  "next_review": "2026-08-18",
  "reviews": 1
}
---

**Q**: 京东新版属性表如何提取？

**A**: `<div class=attrs>` 存在于渲染 DOM。新版通过 unquoted attrs 正则匹配提取，非旧版 CSS class 匹配
