---
{
  "id": "crawler-CSS阻塞什么JS-101",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "CSS 阻塞什么、JS 阻塞什么、卡在哪一步？defer 和 async 区别？为什么 JS 放 body 底部加快首屏？",
  "a": "- **CSS 阻塞渲染树构建（③）；JS 阻塞 DOM 解析（①）**（遇到 `<script>` 阻塞下载执行）\n  - defer = 解析完按文档顺序执行；async = 下载完立即执行不保序；共同点 = 下载都不阻塞解析\n  - JS 放 body 尾 → HTML 先解析完首屏先出；放 head 阻塞 body 解析 → 白屏久",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: CSS 阻塞什么、JS 阻塞什么、卡在哪一步？defer 和 async 区别？为什么 JS 放 body 底部加快首屏？

**A**: - **CSS 阻塞渲染树构建（③）；JS 阻塞 DOM 解析（①）**（遇到 `<script>` 阻塞下载执行）
  - defer = 解析完按文档顺序执行；async = 下载完立即执行不保序；共同点 = 下载都不阻塞解析
  - JS 放 body 尾 → HTML 先解析完首屏先出；放 head 阻塞 body 解析 → 白屏久
