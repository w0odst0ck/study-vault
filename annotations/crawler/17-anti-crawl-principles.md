# 注：反爬对抗原理（17-anti-crawl-principles）

> crawler-learning B4 入库后补注（2026-09-03）

## L1 术语

### 浏览器指纹 [ⓘ]
JS 能读到的环境信息组合（UA/Canvas/WebGL/字体/时区/语言/插件…），组合熵高到能唯一标识一个浏览器。
反爬用指纹识别"同一个浏览器反复来"（封号/封设备比封 IP 更准）。
伪装的关键是**全维度一致**——只改 UA 而 Canvas 指纹不变照样被识别。

### headless（无头浏览器） [ⓘ]
没有可见窗口的浏览器（Playwright headless 模式）。默认带一堆可检测特征：
`navigator.webdriver=true`、无插件、Canvas 渲染结果与有头不同、时区/语言默认值等。
对策：stealth 插件 + 真实指纹参数 + 一致性检查（伪装的深度取决于反爬层级）。
见 [glossary/Playwright](../glossary/Playwright.md)。

## L2 概念

### 四层检测漏斗 [ⓘ]
反爬按"成本递增"分层：请求层（频次/UA/IP，最便宜）→ 特征层（指纹/headless 检测）→ 行为层（轨迹/速度/点击）→ 内容层（验证码/登录墙，最贵）。
先廉价过滤，可疑才升级挑战。**被哪层拦决定换什么招**：请求层换 IP/UA，特征层伪装指纹，行为层模拟真人。
