---
{
  "id": "crawler-CDPChromeD-053",
  "domain": "crawler",
  "source": "knowledge/crawler/12-zkh-waf-bypass.md",
  "q": "CDP（Chrome DevTools Protocol）连接 Windows 真机 Chrome 的架构？",
  "a": "WSL2 Python 通过 CDP 协议连接 Windows 上已打开的真实 Chrome（需 `--remote-debugging-port=9222`），利用其真实浏览器指纹+已登录 Cookie，绕过 WAF 检测。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: CDP（Chrome DevTools Protocol）连接 Windows 真机 Chrome 的架构？

**A**: WSL2 Python 通过 CDP 协议连接 Windows 上已打开的真实 Chrome（需 `--remote-debugging-port=9222`），利用其真实浏览器指纹+已登录 Cookie，绕过 WAF 检测。
