---
{
  "id": "crawler-前端解析器如何防止XS-033",
  "domain": "crawler",
  "source": "knowledge/crawler/08-jd-parser-frontend.md",
  "q": "前端解析器如何防止 XSS？",
  "a": "图片用 `document.createElement('img')` DOM API 构建，禁止 `innerHTML` 拼接商品数据",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 前端解析器如何防止 XSS？

**A**: 图片用 `document.createElement('img')` DOM API 构建，禁止 `innerHTML` 拼接商品数据
