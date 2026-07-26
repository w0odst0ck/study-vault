---
{
  "id": "crawler-WSL2下headl-052",
  "domain": "crawler",
  "source": "knowledge/crawler/12-zkh-waf-bypass.md",
  "q": "WSL2 下 headless Chrome 被 WAF 检测到的原因是什么？",
  "a": "特征包括：user-agent 含 \"HeadlessChrome\"、navigator.webdriver 为 True（即使配置 stealth）、缺少真实 GPU 渲染特征、IP 来源为 WSL2 NAT 网络。WAF 综合判断后对搜索功能拦截。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: WSL2 下 headless Chrome 被 WAF 检测到的原因是什么？

**A**: 特征包括：user-agent 含 "HeadlessChrome"、navigator.webdriver 为 True（即使配置 stealth）、缺少真实 GPU 渲染特征、IP 来源为 WSL2 NAT 网络。WAF 综合判断后对搜索功能拦截。
