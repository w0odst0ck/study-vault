---
{
  "status": "active",
  "created": "2026-07-25",
  "updated": "2026-09-03",
  "tags": [
    "爬虫",
    "WAF",
    "阿里云",
    "反爬",
    "滑块验证码"
  ],
  "cards": [
    "crawler-CDPChromeD-053",
    "crawler-WSL2下headl-052",
    "crawler-ZKH使用的阿里云W-051",
    "crawler-ZKH搜索API路-055",
    "crawler-acw_tcCooki-054"
  ]
}
---

# ZKH 阿里云 WAF 绕过实战

> 来源：price-compare 精简重构（2026-07-25）
> 关键词：AliWAF · aliyun-captcha · CDP · acw_tc · WSL2 反爬

## 背景：ZKH（震坤行）反爬体系

### 检测到的组件

| 防御层 | 技术方案 | 检测点 |
|--------|---------|--------|
| Web 应用防火墙 | **AliWAF**（阿里云） | 请求特征、User-Agent、IP 信誉 |
| 滑块验证码 | **aliyun-captcha** | 行为验证，触发后阻断搜索 |
| 浏览器指纹 | Headless 检测 | WSL2 Chrome 无头模式被拦截 |

### 难度评估

```yaml
页面内容采集: 可行（已验证）
搜索功能调用: 被 AliWAF 拦截（即使有 Cookie）
真实搜索 API: 路径未知，探测返回 404/401
```

## 核心问题：WSL2 + Headless 检测

### 问题定位

WSL2 环境下 Playwright 启动的 headless Chrome：

```
特征：
- user-agent 含 "HeadlessChrome" 或异常
- navigator.webdriver 为 True（即使配置 stealth）
- 缺少真实显卡/GPU 渲染特征
- IP 来源为 WSL2 NAT 网络
```

WAF 检测到这些特征后：
1. 正常页面 √（仍可访问）
2. 搜索触发 → 验证码 → 阻断 ✗

### 方案演进

```
方案 A（失败）：Playwright 搜索 → WAF 拦截
方案 B（失败）：page.evaluate 中 fetch 搜索 API → 401/404
方案 C（有效）：CDP 连接 Windows 真机 Chrome
方案 D（待验证）：复制到 Windows 桌面直接运行
```

## CDP（Chrome DevTools Protocol）方案

### 连接架构

```
WSL2 (Python) ──CDP──→ Windows Chrome（已登录 ZKH）
                             │
                          acw_tc Cookie（有效）
                             │
                          真实浏览器指纹
                             │
                          无 WAF 拦截
```

### 实现要点

```python
# 连接 Windows 上已打开的 Chrome
import subprocess
from playwright.sync_api import sync_playwright

# Windows 端启动 Chrome（需开启远程调试端口）
# chrome.exe --remote-debugging-port=9222

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://192.168.x.x:9222")
    # 使用已登录的浏览器上下文
    context = browser.contexts[0]
    page = context.new_page()
```

### 前提条件

1. Windows Chrome 需以 `--remote-debugging-port=9222` 启动
2. WSL2 与 Windows 需在同一局域网（默认可达）
3. Windows Chrome 上需预先登录 ZKH 并完成一次滑块验证

## Cookie 策略：acw_tc

### 提取与保存

```
来源：Windows Chrome 已登录会话
提取：手动从 DevTools → Application → Cookies → acw_tc
保存：cookies/cookies_zkh.json
有效期：约 7 天（过期需重新提取）
```

### 使用模式

```python
# config 中配置 Cookie 文件路径
config.cookie_file = "cookies/cookies_zkh.json"

# 启动时加载
def setup_session():
    cookies = load_cookies()
    context.add_cookies(cookies)
```

## 搜索 API 路径探测

### 探测结果

| 探测路径 | 状态 | 说明 |
|---------|------|------|
| `/servezkhApi/product/search` | 401 | 存在但需认证 |
| `/servezkhApi/product/list` | 404 | 不存在 |
| `/api/search` | 404 | 不存在 |
| `/search` | 200 | 页面存在，WAF 触发 |

### 待解决问题

- 真实搜索 API 路径需通过 Playwright 请求拦截捕获
- HTTP 请求拦截 vs CDP 请求拦截（CDP 下 Playwright 拦截不稳定）
- 可选方案：Windows 桌面运行 `probe_api_v2.py` 捕获真实请求

### 恢复策略

```
跑通 Windows 桌面 → 记录搜索 API 路径 →
提取请求参数（query/keyword/page）→
迁移回 WSL → 模拟 API 调用（带 Cookie + 正确 Header）
```

## 回顾
<!-- cards: crawler-CDPChromeD-053, crawler-WSL2下headl-052, crawler-ZKH使用的阿里云W-051, crawler-ZKH搜索API路-055, crawler-acw_tcCooki-054 -->
<!-- cards: crawler-CDPChromeD-053, crawler-WSL2下headl-052, crawler-ZKH使用的阿里云W-051, crawler-ZKH搜索API路-055, crawler-acw_tcCooki-054 -->
<!-- cards: crawler-CDPChromeD-053, crawler-WSL2下headl-052, crawler-ZKH使用的阿里云W-051, crawler-ZKH搜索API路-055, crawler-acw_tcCooki-054 -->
<!-- cards: crawler-ZKH使用AliWAF滑块验证码的检-051, crawler-WSL2headlessChrome被WAF检测-052, crawler-CDP连接Windows真机Chrome-053, crawler-acw_tcCookie生命周期约7天-054, crawler-ZKH搜索API路径探测策略-055 -->
- Q: ZKH 使用的阿里云 WAF 防御体系包括哪些组件？
  A: AliWAF（Web 应用防火墙）、aliyun-captcha（滑块验证码）、浏览器指纹检测（Headless 模式），三层叠加。页面浏览可通过，搜索功能触发验证码阻断。

- Q: WSL2 下 headless Chrome 被 WAF 检测到的原因是什么？
  A: 特征包括：user-agent 含 "HeadlessChrome"、navigator.webdriver 为 True（即使配置 stealth）、缺少真实 GPU 渲染特征、IP 来源为 WSL2 NAT 网络。WAF 综合判断后对搜索功能拦截。

- Q: CDP（Chrome DevTools Protocol）连接 Windows 真机 Chrome 的架构？
  A: WSL2 Python 通过 CDP 协议连接 Windows 上已打开的真实 Chrome（需 `--remote-debugging-port=9222`），利用其真实浏览器指纹+已登录 Cookie，绕过 WAF 检测。

- Q: acw_tc Cookie 的提取和使用策略是什么？
  A: 从 Windows Chrome DevTools → Application → Cookies 手动提取，保存到 cookies/cookies_zkh.json。有效期为约 7 天，过期需重新提取。启动时通过 load_cookies() 加载到浏览器上下文。

- Q: ZKH 搜索 API 路径探测的策略和结果？
  A: 探测到 `/servezkhApi/product/search` 返回 401（存在但需认证），其他路径返回 404。真实搜索 API 需通过 Playwright 请求拦截捕获（在 Windows 桌面环境运行 probe_api_v2.py），跑通后记录参数格式，迁移回 WSL 模拟调用。
