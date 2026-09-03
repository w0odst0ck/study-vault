---
{
  "id": "crawler-URL到商品卡片显示-106",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "URL 到商品卡片显示，按顺序说每一步？JS/CSS 分别在哪个环节介入？",
  "a": "- 完整 10 步：下载 HTML → 解析①遇 `<script>` 阻塞下载执行 JS（React 跑起来）→ JS 用 XHR/fetch 请求商品数据 → 改 DOM → ②CSSOM → ③渲染树 → ④布局 → ⑤绘制合成 → 卡片显示\n  - **JS 卡①（DOM 解析）；CSS 卡③（渲染树构建）**——别搞混",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: URL 到商品卡片显示，按顺序说每一步？JS/CSS 分别在哪个环节介入？

**A**: - 完整 10 步：下载 HTML → 解析①遇 `<script>` 阻塞下载执行 JS（React 跑起来）→ JS 用 XHR/fetch 请求商品数据 → 改 DOM → ②CSSOM → ③渲染树 → ④布局 → ⑤绘制合成 → 卡片显示
  - **JS 卡①（DOM 解析）；CSS 卡③（渲染树构建）**——别搞混
