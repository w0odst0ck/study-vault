---
status: active
created: 2026-07-17
updated: 2026-07-20
tags:
  - 爬虫
  - 反爬
  - B2B
  - "1688"
  - 震坤行
cards:
  - crawler-1688搜索页弹出的滑-001
  - crawler-反爬安全策略配置中ra-004
  - crawler-震坤行搜索页的SSR-002
  - crawler-震坤行的阿里云WAF-003
---

# B2B 工业品平台反爬实战

> 来源：price-compare、PH(震坤行选品)、BriefNexus 项目实战
> 日期：2026-07

## 各平台防护等级

| 平台 | 防护层 | 难度 | IP冷却[ⓘ] |
|------|--------|------|--------|
| **1688** | 滑块验证码[ⓘ] + 账号风控 | 🔴高 | 1-3天 |
| **震坤行(ZKH)** | Cloudflare + 阿里云WAF | 🔴高 | 24h |
| **京东** | SPA架构 + 账号封禁 | 🔴高 | 视违规程度 |
| **东方财富** | 418反爬 | 🟡中 | — |
| **巨潮资讯** | 403 IP封禁 | 🟡中 | — |
| **央行** | Connection Reset | 🟡中 | — |
| **标准信息平台(SAMR)** | 速率限制 | 🟢低 | 冷却后恢复 |

## 1688 反爬要点

### 滑块验证码
- 直接访问 `s.1688.com/selloffer/offer_search.htm` 弹出滑块
- 解法：Playwright 滑块等待模式 `wait_for_captcha_solve()`
- 流程：一次过滑块 → 保存 state → 复用

### 搜索入口
- 主页搜索框交互：回车键不触发，需显式点击搜索按钮
- 采购助手插件 XLSX 导出可作为主力数据源

### 账号冷却
- 多次 reload 触发风控
- 冷却 1-3 天，冷却后一次过滑块存 state

## 震坤行(ZKH) 反爬要点

### 阿里云 WAF（遮罩层）
- 遮罩 `#waf_nc_block[ⓘ]` 拦截 pointer events
- 解法：`MutationObserver` 预移除遮罩

### Cloudflare 保护
- 搜索页 `/search.html?keywords=xxx` 有 CF 保护
- 首页 **没有** CF 保护（可首页进再从搜索框交互）

### SSR 数据提取（关键发现）
- 搜索 URL 格式：`/search.html?keywords={keyword}`（非 `/search?keyword=xxx`）
- **搜索结果通过 `window.__INITIAL_DATA__[ⓘ]` JSON 嵌入 HTML**
- 字段映射：
  - `proSkuProductName` → 标题
  - `proBrandName` → 品牌
  - `proMaterialNo` → 型号
  - `proSkuNo` → 编码
- 价格在 DOM: `.sku-price-wrap-new .integer` + `.decimal`
- API 前缀：`/servezkhApi/search/*`

### IP 风控
- 多次探测后 IP 拉黑，首页也进不去
- 需换 IP 或等 24h 冷却

## 通用反爬策略

```python
# 反爬安全策略配置
crawl_config = {
    "request_delay": (0.5, 2.0),      # 自适应延时
    "exponential_backoff[ⓘ]": True,       # 指数退避
    "risk_detection": True,            # 风控检测
    "rate_limit": "10 req/min",        # 限速保护
    "ua_rotation": True,               # UA 轮换
    "stealth_js": True,                # 隐藏 headless 特征
    "cookie_persistence": True,        # Cookie 持久化
    "session_isolation[ⓘ]": True,         # 跨平台 Session 隔离
}
```

### Playwright 浏览器管理器核心设计
详见 [02-playwright-browser-manager.md](02-playwright-browser-manager.md)

### 共享反检测库 `lib/stealth.py`

2026-07-20 从各项目（PageHarvest/price-compare/factory-monitor）提取公共反检测逻辑到共享 `lib/stealth.py`：

- e2e 管道拦截（遮挡 `navigator.webdriver` 等特征）
- WebDriver 属性清除
- 视图端口随机化
- 时间区/语言环境伪装
- 字体指纹伪装
- 通过 `import lib.stealth` 单行引用即可生效

**设计原则：** 一处维护，多处受益。修改反检测策略仅改一处。

### 1688 Playwright 采集器升级（requests → Playwright）

price-compare 项目 1688 采集器（2026-07-20）：

- 原因：requests 直连 1688 搜索页必然触发滑块验证码
- Playwright 策略：加载页面 → 等待滑块 → 用户一次过验证 → 保存 state → 复用
- 解析逻辑与纯前端解析器保持接口一致，解析代码可双向复用
- 详见 [07-client-side-parser-architecture.md](07-client-side-parser-architecture.md)

## 工业品爬虫平台选择

- **T1(活跃)**：1688、震坤行(ZKH)
- **T2(规划)**：京东工业品
- **T3(储备)**：工品汇、西域、固安捷、百度爱采购、慧聪网

> 只专注 B2B 工业品平台，不做消费品（京东零售/天猫/淘宝等）

## 回顾
<!-- cards: crawler-1688搜索页弹出的滑-001, crawler-反爬安全策略配置中ra-004, crawler-震坤行搜索页的SSR-002, crawler-震坤行的阿里云WAF-003 -->
<!-- cards: crawler-1688搜索页弹出的滑-001, crawler-反爬安全策略配置中ra-004, crawler-震坤行搜索页的SSR-002, crawler-震坤行的阿里云WAF-003 -->
- Q: 1688 搜索页弹出的滑块验证码如何解决？
  A: 使用 Playwright 的 `wait_for_captcha_solve()` 等待用户手动通过滑块，一次性过滑块后保存浏览器 state 文件，后续复用避免重复弹出。
- Q: 震坤行搜索页的 SSR 数据提取关键字段映射是什么？
  A: 搜索结果通过 `window.__INITIAL_DATA__` JSON 嵌入 HTML，字段映射：`proSkuProductName`→标题、`proBrandName`→品牌、`proMaterialNo`→型号、`proSkuNo`→编码。
- Q: 震坤行的阿里云 WAF 遮罩层如何绕过？
  A: 使用 `MutationObserver` 在遮罩元素 `#waf_nc_block` 插入 DOM 之前将其预移除，避免拦截 pointer events。
- Q: 反爬安全策略配置中 rate_limit 的典型值是多少？
  A: 典型限速为 10 req/min，配合自适应延时 `request_delay: (0.5, 2.0)` 和指数退避使用。
