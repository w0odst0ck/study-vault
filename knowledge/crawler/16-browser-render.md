---
{
  "status": "active",
  "created": "2026-09-03",
  "updated": "2026-09-03",
  "source": "crawler-learning",
  "tags": [
    "爬虫",
    "渲染"
  ],
  "cards": [
    "crawler-CSS阻塞什么JS-101",
    "crawler-React商品页re-105",
    "crawler-URL到商品卡片显示-106",
    "crawler-requests打-108",
    "crawler-商品数据存在于哪里re-107",
    "crawler-无头浏览器vsreq-103",
    "crawler-渲染树vsDOM树-099",
    "crawler-渲染管线五步每步产物-098",
    "crawler-用渲染管线解释Reac-100",
    "crawler-采集决策三步口诀为什么-104",
    "crawler-重排vs重绘col-102"
  ]
}
---

# B3 浏览器与渲染 知识手册

> 用途：**学习/查阅**——知识点常新常查。
> 配套：错题复习 → B3-quiz.md ｜ 过程回溯 → B3-review.md
> 承接：B2 解析（DOM/CSR/SPA）→ 本阶段深挖"浏览器怎么把页面画出来" + 无头浏览器原理。

## 目录

1. [必答问题](#1-必答问题)
2. [第 1 课 渲染管线：URL 到像素](#2-第-1-课-渲染管线url-到像素)
3. [第 2 课 CSSOM 与渲染阻塞](#3-第-2-课-cssom-与渲染阻塞)
4. [第 3 课 布局与绘制：重排/重绘](#4-第-3-课-布局与绘制重排重绘)
5. [第 4 课 CDP 与无头浏览器](#5-第-4-课-cdp-与无头浏览器)
6. [第 5 课 动态采集实战决策](#6-第-5-课-动态采集实战决策)
7. [B3 总览图（毕业评审标准答案）](#7-b3-总览图毕业评审标准答案)
8. [参考要点](#8-参考要点)
9. [误解纠正](#9-误解纠正)
10. [费曼：一句话讲给外行](#10-费曼)

---

## 1. 必答问题

> 开课时定 3-5 题，读完能答 = 掌握。答不出 → 回对应章节重读。

1. 从输入 URL 到屏幕出像素，浏览器做了哪几步？（渲染管线全貌）
2. CSS 和 JS 为什么阻塞渲染？defer/async 怎么绕过？
3. 重排（reflow）和重绘（repaint）是什么？为什么影响性能？
4. 无头浏览器是什么原理？Playwright 和 requests 的本质差别？
5. 动态页面采集：什么时候必须上 Playwright？代价是什么？

## 2. 第 1 课 渲染管线：URL 到像素

> 场景：B2 学了"CSR 空壳"——requests 拿到京东页只有 `<div id="app">`。追问：JS 执行完了，浏览器到底是怎么把 React 生成的商品卡片**画到屏幕上**的？这中间过了几道工序？

**一句话**：浏览器把 HTML/CSS 变成"看得见的画面"要过五道工序：**解析 HTML → DOM（结构）→ 解析 CSS → CSSOM（样式）→ 合并成渲染树 → 布局算位置 → 绘制+合成画出来**。

### 五步管线

| 步骤 | 产物 | 干什么 | 类比 |
|------|------|--------|------|
| ① 解析 HTML | DOM 树 | 把文本变成结构树（B2 已学） | 列食材清单 |
| ② 解析 CSS | CSSOM 树 | 样式规则也建成树（选择器→样式映射） | 定菜谱 |
| ③ 合并 | 渲染树 Render Tree | DOM + CSSOM 合并，**只留可见元素**（`display:none` 剔除） | 挑要上桌的菜 |
| ④ 布局 Layout | 布局树/几何信息 | 计算每个节点的**位置和尺寸**（宽高/坐标） | 摆盘定位 |
| ⑤ 绘制+合成 | 像素 | 逐层画出来（Paint），分层交给 GPU 合成（Composite） | 上菜 |

### 关键点

- **CSSOM 是什么**：CSS 对象模型，和 DOM 平行的树——CSS 规则（`.offer-title { color: red }`）按选择器建成的映射树。没有它浏览器不知道元素长什么样。
- **渲染树 ≠ DOM 树**：渲染树只含**可见**元素（`display:none` 的、`<head>` 里的都不在）；DOM 树是全量结构。数节点时数的是 DOM，画图时用的是渲染树。
- **布局 ≠ 绘制**：布局算"在哪、多大"（数字），绘制才"涂颜色画出来"（像素）。两者分开，改位置触发布局，只改颜色触发绘制——性能差在这（第 3 课）。
- **JS 在哪一步**：JS 在解析 HTML 时执行（遇到 `<script>` 阻塞解析），执行后**改 DOM** → 重新走 ③④⑤。React 商品卡片就是这么动态出现的：JS 读商品 ID → 生成 DOM 节点 → 触发布局/绘制 → 画面更新。
- **CSR 为什么空壳**：requests 拿到的是**第 ① 步的原始 HTML**（只有挂载点），商品卡片要等 JS 执行（浏览器里才有）——请求层根本没有后续步骤可走。**不是解析器不行，是数据在浏览器里才生成**。

### PH 落点

- 京东/1688 React 页 = CSR：requests 只能拿到空壳 → 必须上 Playwright（第 4 课讲原理）。
- PH 前端解析器面对的是"用户拖进来的完整 HTML"（油猴采集时 JS 已跑完）→ 解析器只需要 ① 的产物（DOM），不需要渲染管线——所以纯前端解析可行。
- 判断一个页面能不能纯 requests：看 HTML 里有没有数据（响应体原文归类，B2-10 的标准答案）——空壳 → 上 Playwright。

**微题**：B3-quiz.md 批次 20。

## 3. 第 2 课 CSSOM 与渲染阻塞

> 场景：为什么有些网页打开会**白屏几秒**？为什么优化教程都说"CSS 放 head、JS 放 body 尾"？

**一句话**：CSS 和 JS 是两类**渲染阻塞资源**——CSS 阻塞**渲染树构建**（卡在第 ③ 步，CSS 不全页面不画），JS 阻塞 **DOM 解析**（卡在第 ① 步，遇到 `<script>` 就暂停）。

### 两类阻塞

| 资源 | 阻塞什么 | 卡在哪 | 为什么 |
|------|---------|--------|--------|
| CSS（`<link>`） | 渲染树构建/首帧 | 第 ③ 步 | 渲染树 = DOM + **完整 CSSOM** 合并；CSS 没下完就没有完整 CSSOM，浏览器不画第一帧 → 白屏 |
| JS（`<script>`） | DOM 解析 | 第 ① 步 | 解析器遇到同步 `<script>` **暂停解析、先执行 JS**（可能改 DOM），执行完才继续解析后续 HTML |

### 绕过：defer / async

| 属性 | 下载 | 执行时机 | 顺序 | 适用 |
|------|------|---------|------|------|
| `defer` | 不阻塞解析 | HTML 解析完（DOMContentLoaded 前） | 按文档顺序 | 依赖 DOM 的脚本（React 主包） |
| `async` | 不阻塞解析 | 下载完**立即**执行 | 不保证 | 独立脚本（统计/广告） |

- 两者共同点：**下载都不阻塞 HTML 解析**；区别在执行时机与顺序保证。
- 没有属性：同步执行，既阻塞下载也阻塞执行。

### 关键点

- **为什么 CSS 放 head**：HTML 是流式解析的，CSS 放 head 让浏览器**尽早发现并下载** CSS（和 HTML 并行），等 body 解析完 CSS 也好了 → 不白屏。放 body 尾 → 解析完了才遇到 CSS → 先画无样式内容再重绘（FOUC 闪烁）。
- **为什么 JS 放 body 尾**：放 head 里会阻塞解析——整个 body 要等 JS 下载执行完才开始解析 → 白屏更久。放尾部 → HTML 先解析完（首屏内容先出来），JS 最后执行。
- **爬虫视角**：白屏/首屏慢 = CSS/JS 加载问题；但爬虫要的不是"快"是"数据在不在"——CSR 页面即使白屏，JS 也执行了（数据在内存/网络请求里），等元素出现即可抓。

### PH 落点

- Playwright 采集 CSR 页：用 `wait_for_selector` / 网络空闲等待，别用固定 sleep——等"渲染产物"出现，不是等时间（第 5 课展开）。
- 京东页面观察：React 主包是 defer 还是 async？为什么首屏能那么快出内容（SSR 部分）？

**微题**：B3-quiz.md 批次 21。

## 4. 第 3 课 布局与绘制：重排/重绘

> 场景：为什么浏览器调优都说"别频繁改样式"？为什么动态插入商品卡片列表会卡？

**一句话**：改样式会触发两类开销——改**几何**（尺寸/位置）触发**重排**（重新算布局，贵），只改**外观**（颜色/背景）触发**重绘**（重画像素，便宜）；只动 `transform/opacity` 走**合成**（GPU，最便宜）。

### 三档开销

| 操作 | 触发的活 | 管线步骤 | 成本 |
|------|---------|---------|------|
| 改 color/background/visibility | 重绘 repaint | ⑤ 画一遍 | 中 |
| 改 width/height/margin/position/display、DOM 增删 | 重排 reflow（=重新布局） | ④ 重算几何 + ⑤ 重画 | 贵 |
| 只动 transform/opacity | 合成 composite | 跳过 ④⑤，直接图层合成 | 最便宜 |

### 关键点

- **重排一定伴随重绘，重绘不一定重排**：改 width → 先重排再重绘；改 color → 只重绘。
- **重排是全局的**：一个元素尺寸变了，可能影响兄弟/父节点/整个文档 → 浏览器重新算整棵布局树（或子树）。
- **读几何也会触发重排**：`offsetWidth / scrollTop / getBoundingClientRect()` 读到的是"当前"布局——如果之前有改样式的操作没生效（浏览器懒批次），读的时候被迫**先排一次**（强制同步布局，forced reflow）。
- **为什么"先读后写"是优化**：连续写 100 次样式 = 浏览器合并成一次重排；中间插读 = 每次读都强制同步 → 100 次重排。
- **批量插入用 DocumentFragment**：一次性挂到 DOM，只触发一次重排，而不是逐个插入触发 N 次。

### PH 落点

- 滚动加载/懒加载 = 动态插入商品卡 → 每次插入触发重排——页面卡顿的常见来源（前端采集器不用管，但理解"为什么页面卡"有助于判断页面状态）。
- 爬虫侧：Playwright 抓取时页面在持续重排（懒加载）→ 等元素稳定再抓；`wait_for_selector` 等的是 DOM 出现，重排不影响抓取，但滚动要等新元素渲染完。

**微题**：B3-quiz.md 批次 22。

## 5. 第 4 课 CDP 与无头浏览器

> 场景：你用过 Playwright/Selenium——"模拟正常 Chrome"。追问：它到底怎么模拟的？为什么能执行 JS 而 requests 不能？

**一句话**：无头浏览器 = **没有界面的完整浏览器**（完整 HTML/CSS/JS 引擎 + 完整渲染管线）；Playwright 通过 **CDP**（Chrome DevTools Protocol，Chrome 暴露的调试协议，DevTools 就是用它）控制 Chromium，让页面真正"跑起来"。

### 前置：XHR/fetch 是什么（批次 23 补课）

- **XHR**（XMLHttpRequest）：浏览器里 JS 发 HTTP 请求的老牌 API（1999 年起），Ajax 的核心。写法啰嗦：`xhr.open('GET', url); xhr.send(); xhr.onload = ...`
- **fetch**：2015 年后的新 API，Promise 风格更简洁：`fetch(url).then(r => r.json())`
- 共同点：让 JS **不刷新页面就能向服务器要数据**（异步请求 = Ajax 的本义）。
- **与渲染管线的关系**：CSR 页面数据流 = HTML 空壳 → JS 执行 → **用 XHR/fetch 向服务器要数据（JSON）** → 改 DOM → 重排重绘 → 显示。**商品数据不是"渲染出来的"，是 XHR/fetch 请求回来的**——所以 DevTools Network 能看到这些请求，拦截 = 拿数据源头。
- **与 requests 的关系**：requests = Python 发 HTTP；XHR/fetch = 浏览器 JS 发 HTTP。同一 HTTP 协议，不同环境的客户端（状态码/头/keep-alive 知识全适用）。

### CDP 是什么

- Chrome/Chromium 暴露的**调试协议**（WebSocket/HTTP），DevTools 界面的每个面板背后都是 CDP 调用。
- 核心域（按用途）：

| 域 | 干什么 | 采集用处 |
|----|--------|---------|
| `Page` | 导航/截图/PDF | 打开页面、截图留证 |
| `Runtime` | 执行任意 JS | `page.evaluate()` 取数据 |
| `DOM` | 操作 DOM | 查/改页面结构 |
| `Network` | 拦截/监听请求响应 | **直接拿 XHR/fetch 的 JSON** |
| `Emulation` | 模拟设备/UA/网络 | 伪装环境 |

### Playwright 怎么工作

1. 启动一个 Chromium 进程（headless）
2. 通过 CDP 连上去（协议是公开的，Puppeteer/Playwright/DevTools 同一套）
3. 你的每个操作（`goto`/`click`/`wait_for_selector`）→ 翻译成 CDP 命令 → 浏览器执行 → 结果回传

### Playwright vs requests：本质差别

| | requests | Playwright |
|---|----------|------------|
| 是什么 | HTTP 客户端 | 驱动完整浏览器 |
| 管线经历 | 只有第 ① 步（原始 HTML） | ①~⑤ 全走 + JS 执行 |
| JS | 不执行 | 完整执行（V8） |
| 拿数据 | 响应体字符串 | DOM 快照 / **网络响应 JSON** / 任意 JS 求值 |
| 代价 | 轻快 | 重（内存/CPU）、慢、易被风控识别 |

### 关键点

- **"模拟 Chrome"的本质 = 真的是 Chrome**：不是假装，是驱动真的浏览器进程干活。风控能识别它，因为"真浏览器"的行为指纹（Canvas/WebGL/字体/时区）和 Playwright 注入的特征可被检测（第 4 课反爬展开，P4 阶段）。
- **动态采集两条路**：① 等渲染完解析 DOM（慢，受布局/懒加载影响）；② **拦截 Network 直接拿接口 JSON**（数据源头，快且稳——前端展示的数据就是它）。很多"难爬"页面，找到 XHR 接口后 requests 都能直接打（B2-7 的 script JSON 思路同源）。
- **Playwright 不等于万能**：CSR 页面优先找接口（轻），接口找不到/加密了再上浏览器（重）。

### PH 落点

- PH 离线解析吃完整 HTML → 不需要浏览器；未来 S3 或 factory-monitor 若碰 CSR 直采，才需要 Playwright（待议）。
- 京东观察：打开 DevTools Network 看商品数据是哪个 XHR 返回的——理解"前端展示 = 接口数据"。

**微题**：B3-quiz.md 批次 23。

## 6. 第 5 课 动态采集实战决策

> 场景：遇到一个页面，怎么决定用 requests 还是 Playwright？无脑上浏览器 = 又慢又重又容易被封。

**一句话**：采集决策由轻到重三步：**先 HTML、再接口、最后浏览器**——数据在 HTML 里直接 requests；空壳就找 XHR/fetch 接口（能打就打 requests）；接口加密/要登录态才上 Playwright。

### 决策流程

```
拿到 URL → 先 GET 看响应体原文（B2-10 第一步）
├─ 数据在 HTML 里 → requests 直接解析 ✅（轻）
├─ 空壳 CSR → DevTools Network 找 XHR/fetch 接口
│   ├─ 接口能直接打（无加密/无签名）→ requests 打接口 ✅（轻）
│   └─ 接口加密/签名/要登录态 → Playwright ⚠️（重）
└─ 登录墙/风控 → 先解决凭证（S3），再按上面走
```

### Playwright 实战要点

| 场景 | 做法 | 别用 |
|------|------|------|
| 等渲染 | `wait_for_selector(元素)` / `wait_for_load_state('networkidle')` | 固定 `sleep(3)`——快慢机器/网络波动下要么白等要么抓空 |
| 懒加载 | 滚动触发（`mouse.wheel` / `evaluate` scrollTo），滚动后**再等新元素出现**再抓 | 一次性抓完——后面的商品没渲染 |
| 拿数据 | `page.evaluate` 取 DOM / `page.route` 拦截响应 JSON | 只刮 DOM——数据源头在响应里 |
| 超时 | 每个等待设超时 + 重试 | 无限等 |

### 关键点

- **为什么等元素不 sleep**：sleep 是猜时间，`wait_for_selector` 是等"渲染产物"出现——网络快慢/机器快慢都不怕，出现才继续。
- **懒加载三件套**：滚动 → 等新元素 → 再抓。滚动一次只渲染一批，要循环滚到底（检测"没有更多"标记）。
- **Playwright 代价清单**：内存（每个浏览器实例几百 MB）、速度（每页秒级 vs requests 毫秒级）、稳定性（超时/元素变动/弹窗）、风控（headless 可被检测，P4 展开）。
- **决策口诀**：由轻到重，能不重就不重——接口方案 = requests 的轻 + 数据的稳。

### PH 落点

- PH 当前路线（油猴采集完整 HTML → 离线解析）天然绕开此问题：采集器在浏览器里跑（用户已登录），解析器吃完整 HTML。
- 未来若做"在线直采"（factory-monitor 修复时机后议）：CSR 站点优先找接口，接口不行再 Playwright。

**微题**：B3-quiz.md 批次 24。

## 7. B3 总览图（毕业评审标准答案）

### 钩子池（深入一问登记，毕业评审组卷素材）

| # | 钩子 | 来源 | 状态 |
|---|------|------|------|
| H1 | 京东 React 主包是 defer 还是 async？为什么首屏能那么快（SSR 部分）？ | 第 2 课 PH 落点 | 待揭晓 |
| H2 | 京东商品数据是哪个 XHR/fetch 接口返回的？参数带什么（签名？）？ | 第 4 课 PH 落点 | 待揭晓 |
| H3 | 风控识别 headless 的具体指纹有哪些（Canvas/WebGL/字体/时区）？怎么测？ | 第 4 课关键点（P4 预告） | 待揭晓 |
| H4 | Playwright 拦截响应 JSON 的 page.route 具体怎么用（含修改响应）？ | 第 5 课实战要点 | 待揭晓 |

### 渲染管线全图

```
① 解析 HTML → DOM 树（结构）
② 解析 CSS  → CSSOM 树（样式）      ← CSS 阻塞③（CSS 不全不合并，白屏）
③ 合并      → 渲染树（只含可见元素）
④ 布局      → 几何信息（位置/尺寸）  ← 改几何=重排（贵）
⑤ 绘制+合成 → 像素（Paint + GPU 合成）← 改外观=重绘；只动 transform/opacity=合成（最便宜）

JS 介入点：解析 HTML 时遇到 <script> 阻塞解析并执行（卡①）→ 改 DOM → 重走③④⑤
前置：XHR/fetch = 浏览器 JS 发 HTTP 请求（Ajax）；CSR 商品数据=接口 JSON，不是从空壳 HTML 解析
```

### 采集决策流（由轻到重）

```
GET 看响应体原文（第一步！）
├─ 数据在 HTML → requests 直接解析
├─ 空壳 CSR → DevTools Network 找 XHR/fetch 接口
│   ├─ 接口无防护 → requests 打接口（轻+稳）
│   └─ 接口签名/加密/要登录 → Playwright（重）
└─ 登录墙 → 先凭证（S3）
```

### Playwright 要点

- 等：`wait_for_selector` / `wait_for_load_state('networkidle')`——等渲染产物，不猜时间（sleep 会抓空）
- 拿：`page.evaluate` 取 DOM / `page.route` 拦截响应 JSON（数据源头优先）
- 懒加载：滚动 → 等新元素出现 → 抓取 → 循环；新元素不再出现 = 到底
- 原理：CDP（Chrome 调试协议）= Playwright 控制真 Chromium 的通道；"模拟"的实质是驱动真浏览器

### 三方案对比（快/稳/轻/风控）

| 方案 | 快 | 稳 | 轻 | 风控 |
|------|----|----|----|------|
| requests 直接抓 | 最快（毫秒） | 仅静态页 | 最轻 | 易被 UA/频率检测（无浏览器特征） |
| 打接口 JSON | 快 | 结构化最稳 | 轻 | **看接口防护**：常有签名/加密，与浏览器指纹是两套体系 |
| Playwright | 慢（秒级） | 受渲染/懒加载影响 | 重（几百 MB） | **最易被识别**（headless 指纹+注入特征） |

口诀：**先 HTML、再接口、最后浏览器**；能不重就不重。

### 必答问题标准答案索引

1. 渲染管线五步 → 上图 ①-⑤
2. CSS/JS 阻塞 → ③ vs ①；defer/async 下载不阻塞、执行时机不同
3. 重排/重绘 → ④ vs ⑤；读几何强制同步布局；transform/opacity 走合成
4. 无头浏览器原理 → CDP 驱动真 Chromium；vs requests = 全管线+JS vs 只有①
5. 何时必须 Playwright → 接口加密/要登录/找不到接口时；代价=慢/重/易被识别

## 8. 参考要点

- WHATWG HTML 解析/树构建：B2 §8 已列
- CSS 对象模型（CSSOM）：CSSOM 规范（W3C）
- CDP：https://chromedevtools.github.io/devtools-protocol/
- Playwright：https://playwright.dev

## 9. 误解纠正

> 初学时的错误心智模型 → 被什么证据纠正。最重要的一节。

1. **"JS 在解析 CSS 时介入"** → 错（毕业评审）。JS 在**解析 HTML 时**介入——遇到 `<script>` 阻塞解析并执行（卡①，可能改 DOM）；CSS 阻塞的是**渲染树构建**（卡③）。JS 与 CSS 各堵各的工序。
2. **"CSR 商品数据从空壳 HTML 解析出来"** → 错（毕业评审）。空壳 HTML 里没有商品 ID——商品数据是 JS 执行后用 **XHR/fetch 从接口拿 JSON** 再渲染的。数据源头是接口，不是 HTML。
3. **"Playwright 被风控则 requests/接口也不成功"** → 错（毕业评审）。三个方案风控体系**互相独立**：Playwright = headless 指纹/注入特征（最易被识别）；接口 = 签名/加密防护（与浏览器指纹无关）；requests 直接抓 = UA/频率检测。PW 被识别 ≠ 接口会被拦。

## 10. 费曼

> 一句话讲给外行：讲不清楚 = 没懂。

（结课补）

## 回顾
<!-- cards: crawler-CSS阻塞什么JS-101, crawler-React商品页re-105, crawler-URL到商品卡片显示-106, crawler-requests打-108, crawler-商品数据存在于哪里re-107, crawler-无头浏览器vsreq-103, crawler-渲染树vsDOM树-099, crawler-渲染管线五步每步产物-098, crawler-用渲染管线解释Reac-100, crawler-采集决策三步口诀为什么-104, crawler-重排vs重绘col-102 -->
- Q: 渲染管线五步？每步产物？
  A: ① 解析 HTML → DOM 树 ② 解析 CSS → CSSOM 树 ③ 合并 → 渲染树（只含可见元素）④ 布局 → 几何信息（位置/尺寸）⑤ 绘制+合成 → 像素

- Q: 渲染树 vs DOM 树？display:none 在哪？
  A: DOM = 全量结构（含隐藏元素）；渲染树 = 只含**可见**元素（display:none 在 DOM 但不在渲染树，不占布局）；head 内容也不在渲染树

- Q: 用渲染管线解释：React 页面 requests 拿到空壳？
  A: requests 只经历解析 HTML（第①步），拿到挂载点空壳；②③④⑤ 全在浏览器发生，且 JS 要先执行（阻塞解析后改 DOM）才生成商品卡片——数据在浏览器里才存在

- Q: CSS 阻塞什么、JS 阻塞什么、卡在哪一步？defer 和 async 区别？为什么 JS 放 body 底部加快首屏？
  A: - **CSS 阻塞渲染树构建（③）；JS 阻塞 DOM 解析（①）**（遇到 `<script>` 阻塞下载执行）
  - defer = 解析完按文档顺序执行；async = 下载完立即执行不保序；共同点 = 下载都不阻塞解析
  - JS 放 body 尾 → HTML 先解析完首屏先出；放 head 阻塞 body 解析 → 白屏久

- Q: 重排 vs 重绘？color/width 触发哪个？为什么读 offsetWidth 是性能坑？只动 transform/opacity 为什么不触发？
  A: - 重绘 = 改像素（便宜）；重排 = 改尺寸/位置（贵）；color→重绘 / width→重排
  - 读几何（offsetWidth）→ 此前攒着的样式改动被迫生效 → **强制同步布局**（forced reflow）；先读后写避免反复强迫
  - transform/opacity：**跳过④布局⑤绘制，直接走合成**（GPU 图层），成本最低

- Q: 无头浏览器 vs requests 本质差别？CDP 是什么？Playwright 通过它干什么？为什么拦截网络请求拿 JSON 更好？
  A: - 无头浏览器 = 完整浏览器（执行 JS + 全渲染管线）；requests 只读 HTML（第①步产物）
  - **CDP = Chrome 调试协议**（DevTools 同款通信方式，DevTools 是工具不是协议）；Playwright 启动真 Chromium → CDP 连接 → 操作翻译成 CDP 命令**驱动**浏览器（不是"模拟"——本质是真 Chrome）
  - 拦截 JSON 三优势：① **数据源头**（结构化 JSON，不用从 DOM 抠）② **稳**（不受懒加载/重排/元素变动影响）③ 快（少渲染步骤）；找到接口 requests 都能直接打

- Q: 采集决策三步口诀？为什么接口优先？为什么不用固定 sleep？懒加载页面怎么抓全、怎么知道到底？
  A: - 口诀：**先 HTML → 再接口 → 最后浏览器**；接口优先 = 稳定可靠 + 浏览器慢/被识别
  - sleep = **猜时间**（固定时长，网络波动下白等/抓空）；用 wait_for_selector / wait_for_load_state('networkidle') 等"产物出现"
  - 懒加载：**滚动 → 等新元素 → 抓取 → 循环**；结束条件 = 滚动后新元素不再出现（或"没有更多"标记）→ 停止

- Q: React 商品页 requests 拿到空壳，完整采集流程怎么走？
  A: 看响应体 → 数据不在 → 找 XHR/fetch 接口（DevTools Network）→ JSON 直拿 → 接口有防护 → Playwright：等 wait_for_selector/networkidle，page.evaluate 取 DOM 或 page.route 拦截响应 JSON，懒加载滚动循环

- Q: URL 到商品卡片显示，按顺序说每一步？JS/CSS 分别在哪个环节介入？
  A: - 完整 10 步：下载 HTML → 解析①遇 `<script>` 阻塞下载执行 JS（React 跑起来）→ JS 用 XHR/fetch 请求商品数据 → 改 DOM → ②CSSOM → ③渲染树 → ④布局 → ⑤绘制合成 → 卡片显示
  - **JS 卡①（DOM 解析）；CSS 卡③（渲染树构建）**——别搞混

- Q: 商品数据存在于哪里？requests 拿 HTML 能拿到吗？
  A: 数据存在于**接口 JSON**（XHR/fetch 响应）；HTML 只有 `<div id="root">` 挂载点；requests 不执行 JS → 拿不到（除非数据内联进 HTML）

- Q: requests / 打接口 / Playwright 三方案快稳轻与风控对比？接口防护和浏览器指纹是同一套体系吗？被接口拦换 PW 有用吗？
  A: - requests 直接抓：最快最轻，仅静态页，易被 UA/频率检测；打接口：快/结构化稳/轻，风控看接口防护（签名/加密）；**Playwright：最慢最重，最易被识别**（headless 指纹 + 注入特征）
  - **两套体系**：接口签名/加密防护 ≠ 浏览器指纹；接口打不动 ≠ PW 打不动，PW 被识别 ≠ 接口会被拦
  - 被接口拦换 PW **有用**：接口防护拦裸请求/无签名，PW 走真实浏览器 + 执行 JS，可绕过纯签名防护
