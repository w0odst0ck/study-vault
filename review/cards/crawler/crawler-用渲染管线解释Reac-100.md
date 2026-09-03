---
{
  "id": "crawler-用渲染管线解释Reac-100",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "用渲染管线解释：React 页面 requests 拿到空壳？",
  "a": "requests 只经历解析 HTML（第①步），拿到挂载点空壳；②③④⑤ 全在浏览器发生，且 JS 要先执行（阻塞解析后改 DOM）才生成商品卡片——数据在浏览器里才存在",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 用渲染管线解释：React 页面 requests 拿到空壳？

**A**: requests 只经历解析 HTML（第①步），拿到挂载点空壳；②③④⑤ 全在浏览器发生，且 JS 要先执行（阻塞解析后改 DOM）才生成商品卡片——数据在浏览器里才存在
