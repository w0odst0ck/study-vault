# 注：Playwright [[glossary/Playwright]] 浏览器管理器实战

## L1 术语

### 单例模式 [ⓘ]
全局只有一个实例，所有代码共享同一个浏览器管理器。
防止重复创建浏览器实例浪费资源。

### Stealth JS [ⓘ]
隐藏浏览器自动化痕迹的 JavaScript 注入脚本。
网站可以通过 `navigator.webdriver` 等属性检测你是不是自动化工具。
Stealth JS 就是把这些检测点全部模拟成真人浏览器的样子。

### Context 隔离 [ⓘ]
见 [glossary/Playwright](../glossary/Playwright.md)。
每平台一个独立 BrowserContext，Cookie/Storage/LocalStorage 互不干扰。

## L2 概念

### 三种搜索策略 [ⓘ]
为什么需要三种策略？因为不同平台的防御力度不同：

| 策略 | 适用场景 | 原理 |
|------|---------|------|
| 渲染模式 | SSR 页面（直接在 HTML 里有数据） | 打开 → 等 DOM 渲染 → 取 HTML |
| API 拦截 | SPA 页面（数据靠 API 加载） | 拦截 XHR 请求 → 直接拿 JSON |
| 主页交互 | 首页无保护的平台（绕过 CF） | 从首页进，避免触发搜索页的保护 |

### networkidle vs load [ⓘ]
`waitUntil` 的两个模式：
- `"load"`：页面的 HTML 和静态资源加载完就算完成（快，够用）
- `"networkidle"`：页面所有网络请求都停了才算完成（严格，但长连接会卡死）

WSL2 下 1688 页面有长轮询，`networkidle` 会一直等到超时。

## L3 架构

### 管理器模式 [ⓘ]
不直接操作 Playwright API，而是包装成 `BrowserManager` 类。
好处：跨平台切换（switch_platform）、自动注入 Stealth JS、统一管理登录态。
