# 注：浏览器与渲染（16-browser-render）

> crawler-learning B3 入库后补注（2026-09-03）

## L1 术语

### CSSOM [ⓘ]
CSS 对象模型：样式规则（选择器 → 样式映射）解析成的树，与 DOM 树对应。
渲染五步管线：解析 HTML → DOM → 解析 CSS → **CSSOM** → 合并渲染树 → 布局 → 绘制+合成。
爬虫意义：CSR 页面 requests 拿到的空壳 HTML 没有这些——要"看到画面"必须等 JS 执行完（渲染管线跑完），这就是动态采集要等渲染/用无头浏览器的原因。

### 重排 / 重绘（reflow / repaint） [ⓘ]
- 重排（reflow/layout）：DOM/CSS 变了 → 重新计算位置尺寸（贵）
- 重绘（repaint）：只颜色/可见性变 → 重画（便宜）
爬虫意义：页面反复改 DOM（懒加载/轮播）会触发重排重绘——等页面"稳定"再抓，避免抓到半渲染状态。

## L2 概念

### CSR（客户端渲染） [ⓘ]
页面 JS 在浏览器端渲染，源码 HTML 几乎是空壳（`<div id="app">`），数据靠 XHR/fetch 请求加载。
requests 直接抓 = 拿空壳。对策：无头浏览器渲染完再抓 / 直接抓 XHR API（更快更稳）。
见 [glossary/CSR](../glossary/CSR.md)。
