---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-21",
  "tags": [
    "爬虫",
    "Playwright",
    "浏览器自动化"
  ],
  "cards": [
    "crawler-Playwright浏-009",
    "crawler-StealthJS注-010",
    "crawler-跨平台Context-011"
  ]
}
---

# Playwright 浏览器管理器实战

> 来源：price-compare、BriefNexus 项目实战
> 日期：2026-07

## 核心设计模式：单例浏览器管理器[ⓘ]

```python
class BrowserManager:
    """浏览器管理器，全局单例"""
    
    def __init__(self):
        self.contexts = {}          # 跨平台 context 隔离[ⓘ]
        self.stealth_js = STEALTH_JS
```

### 核心方法

| 方法 | 用途 | 场景 |
|------|------|------|
| `search_render()` | 渲染模式 | 打开页面 → 返回 HTML |
| `search_api()` | API 拦截模式 | 拦截 XHR → 返回 JSON |
| `search_via_homepage()` | 主页搜索交互 | 绕过 CF 保护 |
| `new_page()` | 统一创建页面 | 自动 inject stealth JS |
| `wait_for_captcha_solve()` | 滑块等待 | 1688 等验证码场景 |
| `login()` | 浏览器登录 | 需登录的平台 |
| `switch_platform()` | 跨平台切换 | context 隔离 |

## Stealth JS[ⓘ] 注入

隐藏 headless 特征的核心方案：

```javascript
// 修改 navigator.webdriver
Object.defineProperty(navigator, 'webdriver', { get: () => false });
// 修改 chrome 属性
window.chrome = { ... };
// 添加 plugins
Object.defineProperty(navigator, 'plugins', { get: () => [1,2,3,4,5] });
// 覆盖 permissions query
// 修改 languages, hardwareConcurrency, deviceMemory 等
```

## 三大搜索策略模式

### 1. 渲染模式（直接导航）[ⓘ]
```
搜索页 URL → 打开页面 → wait DOM → 返回完整 HTML
适用：SSR 页面（ZKH search.html）
```

### 2. API 拦截模式
```
导航页面 → 拦截 XHR/fetch 请求 → 返回 JSON
适用：SPA 页面（ZKH API）
```

### 3. 主页交互模式
```
打开首页（绕过 CF）→ 输入搜索框 → 点击按钮 → 等待结果
适用：首页无保护的平台
```

## 跨平台 Context 隔离

```python
# 每个平台独立 browser context
contexts = {
    "1688": { "cookies": ..., "storage": ... },
    "zkh":  { "cookies": ..., "storage": ... },
}

def switch_platform(self, platform: str):
    """切换平台 context，避免 Cookie 串用"""
```

## 登录态管理

- Cookie 持久化：保存到 JSON 文件，启动时加载
- 过期检测：前置检测 + 自动重新登录
- 登录辅助：`login()` 方法弹出登录界面

## WSL2 下注意事项

- `networkidle[ⓘ]` 超时（轮询/长连接），需改用 `domcontentloaded`
- 无 X Server 时无法启动 Chromium headed 模式
- WSL2 文件系统操作需注意跨操作系统路径

## 夸克网盘自动化（特殊场景）

```
标准全文下载流程：
1. bzxz.net 标准详情页 → 提取夸克分享链接
2. 导航到夸克 → 点击"保存到网盘"
3. 桌面端下载 PDF
```

关键发现：
- 夸克页面 `networkidle` 超时，需 `domcontentloaded`
- 分享链接大部分已过期
- 需手动保存登录态 + 批量操作

## 回顾
<!-- cards: crawler-Playwright浏-009, crawler-StealthJS注-010, crawler-跨平台Context-011 -->
<!-- cards: crawler-Playwright浏-009, crawler-StealthJS注-010, crawler-跨平台Context-011 -->
<!-- cards: crawler-Playwright浏-009, crawler-StealthJS注-010, crawler-跨平台Context-011 -->
- Q: Playwright 浏览器管理器的三种搜索策略模式是什么？
  A: 渲染模式（直接导航取 HTML，适用 SSR 页面）、API 拦截模式（拦截 XHR/Fetch 得 JSON，适用 SPA 页面）、主页交互模式（打开首页绕过 CF -> 输入搜索框 -> 点击按钮，适用首页无保护的平台）。
- Q: Stealth JS 注入的核心原理是什么？
  A: 修改 `navigator.webdriver=false`、模拟 `window.chrome` 对象、添加 plugins、覆盖 permissions query、修改 languages/hardwareConcurrency/deviceMemory 等指纹参数。
- Q: 跨平台 Context 隔离的设计目的是什么？
  A: 每个平台独立 browser context，通过 `switch_platform()` 切换，避免 Cookie/Storage 串用导致跨平台风控。
