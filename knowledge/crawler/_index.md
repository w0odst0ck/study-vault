# 爬虫知识文档索引

> 19 篇文档 · B2B 反爬 / Playwright / 标准采集 / PDF 解析 / 情报采集 / 工厂监控 / 前端解析 / 多源采集流水线 / HTTP / 解析 / 渲染 / 反爬原理 / 监控 / 凭证

---

| # | 文档 | 核心内容 | 卡数 |
|---|------|---------|------|
| 01 | [B2B 工业品平台反爬实战](01-b2b-platforms-anti-crawl.md) | 1688/ZKH/京东反爬策略、共享 stealth 库 | 4 |
| 02 | [Playwright 浏览器管理器](02-playwright-browser-manager.md) | 单例管理/Stealth JS/三大搜索模式/跨平台 Context | 3 |
| 03 | [国家标准信息采集](03-national-standard-collection.md) | SAMR/openstd API、适配器架构、FTS5 | 4 |
| 04 | [PDF 参数页定位器](04-pdf-parameter-locator.md) | PyMuPDF 规则定位、OCR 降级、5 模块架构 | 4 |
| 05 | [多源情报采集架构](05-multi-source-intel-collection.md) | 适配器模式、领域分类、跨天去重 | 4 |
| 06 | [1688 工厂监控流水线](06-1688-factory-monitor.md) | 全链路采集/反检测库/工厂 URL 发现 | 6 |
| 07 | [纯前端 JS 解析器架构](07-client-side-parser-architecture.md) | 产品/开源拆分、1688/ZKH 前端解析、4 级图片降级 | 4 |
| 08 | [京东前端解析器](08-jd-parser-frontend.md) | 新旧版兼容/DOMParser 复用/XSS 防护/全量价格 | 6 |
| 09 | [多源采集流水线架构](09-multi-source-collection-pipeline.md) | 三轮递进/5类产出规范/manual机制/配置驱动 | 待抽取 |
| 10 | [索引驱动的素材管理体系](10-index-driven-material-mgmt.md) | 索引驱动素材管理 | 待抽取 |
| 11 | [多厂商采集策略评估](11-vendor-crawl-evaluation.md) | 多厂商采集策略评估 | 待抽取 |
| 12 | [ZKH 阿里云 WAF 绕过实战](12-zkh-waf-bypass.md) | ZKH 阿里云 WAF 绕过 | 待抽取 |
| 13 | [价格监控项目瘦身与重构](13-project-streamlining-strategy.md) | 价格监控项目瘦身重构 | 5 |
| 14 | [HTTP 协议基础](14-http-protocol.md) | HTTP 报文/状态码/ETag/keep-alive/Cookie/反爬限速 | 26 |
| 15 | [HTML 解析](15-html-parsing.md) | HTML 文本 vs DOM/正则局限/解析管线 | 11 |
| 16 | [浏览器与渲染](16-browser-render.md) | 渲染管线/JS 执行/重排重绘/等待策略 | 11 |
| 17 | [反爬对抗原理](17-anti-crawl-principles.md) | 反爬分类/对抗原理（与 01 平台实战互补）| 15 |
| 18 | [价格监控轮询](18-price-monitoring.md) | monitor 轮询器/快照对比/变化检测 | 7 |
| 19 | [凭证管理](19-credential-management.md) | 登录态/Cookie 凭证生命周期管理 | 6 |

> 14-19 来源：crawler-learning 课程（2026-09-03 经 tools/import_learning.py 入库）
