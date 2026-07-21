# 注：B2B 工业品平台反爬实战

## L1 术语

### 滑块验证码 [ⓘ]
网站的一种验证手段，需要用户拖动滑块到指定位置。
1688 的滑块在特定页面触发（如搜索页），不是每次访问都弹。
解法：Playwright 等待人工一次性通过 → 保存 state 文件 → 后续复用。

### `waf_nc_block` [ⓘ]
震坤行使用的阿里云 WAF 遮罩层元素 ID。
原理：在页面上覆盖一层透明遮罩（`pointer-events: none`），看起来页面正常但所有点击事件都被拦截。
解法：用 MutationObserver 在遮罩插入 DOM 前移除。

### `window.__INITIAL_DATA__` [ⓘ]
服务端渲染（SSR [[glossary/SSR]]）的标准做法——服务端把数据直接塞到 HTML 的 `<script>` 标签中。
爬虫可以直接从页面源码提取 JSON，无需额外发 API 请求。
见 [glossary/SSR](../glossary/SSR.md)。

## L2 概念

### IP 冷却 [ⓘ]
爬虫频率过高触发风控后，IP 被暂时封禁，需要等待一段时间才能恢复。
各平台冷却时长不同：1688 1-3 天、震坤行 24h。
冷却期间即使正常访问也会被拦，必须换 IP 或等待。

### 上下文隔离（Session Isolation） [ⓘ]
见 cross-context 工程实践——不同平台用独立的 BrowserContext，
避免 1688 的 Cookie 污染震坤行的登录态。

## L3 架构解读

### 指数退避（Exponential Backoff） [ⓘ]
失败重试策略：第 1 次失败等 1s，第 2 次等 2s，第 3 次等 4s...
指数级增长等待时间，给服务器恢复时间 + 减少被风控概率。
