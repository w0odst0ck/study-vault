---
{
  "status": "active",
  "created": "2026-07-25",
  "updated": "2026-09-03",
  "tags": [
    "爬虫",
    "项目重构",
    "反爬",
    "代码质量"
  ],
  "cards": [
    "crawler-BrowserManag-057",
    "crawler-PROXY_URL配置-058",
    "crawler-Python爬虫中p-059",
    "crawler-WAF移除脚本执行后为-060",
    "crawler-价格监控项目瘦身的核心策-056"
  ]
}
---

# 价格监控项目瘦身与重构

> 来源：price-compare 重构为 ZKH-only（2026-07-25）
> 关键词：项目瘦身 · BrowserManager · PROXY · 键盘事件 · WAF 移除

## 项目瘦身：从多平台到单平台

### 变更概览

```
26 files changed
670 insertions(+)
2276 deletions(-)
```

### 移除的组件

| 组件 | 说明 | 行数 |
|------|------|------|
| alibaba_1688 | 1688 采集模块 | 大量 |
| _template | 模板/测试文件 | 中等 |
| 测试文件 | 无用测试 | 少量 |

### 瘦身原则

1. **确定核心路径** — ZKH 是唯一目标，其他平台全部移除
2. **测试文件只保留核心** — 非关键测试文件删除
3. **模板不落地** — 模板不带到正式代码中
4. **配置文件清晰** — config 只保留 ZKH 相关配置

## BrowserManager 重构

### 旧方案：setup_session 函数

```python
# 旧：函数式散落，难以复用
def setup_session():
    # ... 100 行各种初始化和 Cookies 加载
    # 问题：check_state_fresh 存在死代码
    # 早期 return 跳过了过期检查
    pass
```

### 新方案：BrowserManager 类

```python
# 新：面向对象管理浏览器生命周期
class BrowserManager:
    def __init__(self, proxy=None):
        self.proxy = proxy
        self.browser = None
        
    def setup_session(self):
        """统一浏览器初始化入口"""
        self._load_cookies()
        self._apply_stealth()
        
    def check_session(self):
        """自动检测 Cookie 是否过期"""
        # 原来 check_state_fresh 有死代码：
        # 早期 return 导致跳过过期检查
        # 修复后改为 _check_session()
```

### 修复的关键 bug

```
check_state_fresh 死代码：
  → 函数开头有早期 return，跳过了 Cookie 过期检查
  → 修复：删除死代码，创建 _check_session() 方法
  → main 入口新增自动检查
```

## PROXY_URL 配置模式

### 实现

```python
# config
PROXY_URL = "http://proxy.example.com:8080"
# 可通过环境变量覆盖
import os
PROXY_URL = os.environ.get("HTTPS_PROXY", PROXY_URL)

# browser 初始化
browser_manager = BrowserManager(proxy=config.PROXY_URL)
```

### 设计要点

1. 配置文件中定义默认值
2. 环境变量覆盖（HTTPS_PROXY）
3. 不影响无代理运行（PROXY_URL 为空时自动跳过）
4. 代理对所有浏览器请求生效（包括页面和 API 请求）

## 爬虫常见坑

### Playwright 键盘事件跨平台差异

```
错误：page.keyboard.select_all()
错误信息：不存在 select_all 方法

修复：page.keyboard.press('Control+a')
注：Windows 用 Control，macOS 用 Meta
```

### WAF 移除脚本的 Ant Design 兼容

```
问题：WAF 移除脚本执行后，Ant Design 弹窗（Modal）未关闭
     导致后续操作被弹窗阻挡

修复：在 WAF 移除脚本末尾增加：
```javascript
// 关闭所有 Ant Design Modal
document.querySelectorAll('.ant-modal-close').forEach(el => el.click());
```
## 回顾
<!-- cards: crawler-BrowserManag-057, crawler-PROXY_URL配置-058, crawler-Python爬虫中p-059, crawler-WAF移除脚本执行后为-060, crawler-价格监控项目瘦身的核心策-056 -->
<!-- cards: crawler-BrowserManag-057, crawler-PROXY_URL配置-058, crawler-Python爬虫中p-059, crawler-WAF移除脚本执行后为-060, crawler-价格监控项目瘦身的核心策-056 -->
<!-- cards: crawler-BrowserManag-057, crawler-PROXY_URL配置-058, crawler-Python爬虫中p-059, crawler-WAF移除脚本执行后为-060, crawler-价格监控项目瘦身的核心策-056 -->
<!-- cards: crawler-价格监控项目瘦身策略移除无-056, crawler-BrowserManager取代setup_ses-057, crawler-PROXY_URL配置模式环境变量-058, crawler-Python爬虫中pagekeyboard-059, crawler-WAF移除脚本需额外关闭Ant-060 -->
- Q: 价格监控项目瘦身的核心策略是什么？
  A: ① 确定 ZKH 为核心路径，移除 alibaba_1688/_template/测试文件；② 测试文件只保留核心；③ 模板不带到正式代码；④ 配置文件只保留 ZKH 相关。共 26 文件变更，-2276 行/+670 行。

- Q: BrowserManager 取代 setup_session 函数解决了什么问题？
  A: 旧函数式散落难以复用，且 check_state_fresh 存在死代码（早期 return 跳过 Cookie 过期检查）。新方案用面向对象封装浏览器生命周期，创建 _check_session() 方法自动检测 Cookie 是否过期。

- Q: PROXY_URL 配置模式的设计要点？
  A: config 文件中定义默认值，同时支持 HTTPS_PROXY 环境变量覆盖，PROXY_URL 为空时自动跳过代理。代理对浏览器所有请求（页面+API）生效，不影响无代理运行。

- Q: Python 爬虫中 page.keyboard.select_all() 的错误原因和正确写法？
  A: Playwright 没有 `select_all()` 方法，应使用 `page.keyboard.press('Control+a')`（Windows）或 `page.keyboard.press('Meta+a')`（macOS）。

- Q: WAF 移除脚本执行后为什么需要额外处理 Ant Design 弹窗？
  A: WAF 移除脚本成功执行后，Ant Design Modal（弹窗）可能仍处于打开状态，阻挡后续操作。需要在脚本末尾增加 `document.querySelectorAll('.ant-modal-close').forEach(el => el.click())` 关闭所有弹窗。
