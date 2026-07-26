---
{
  "id": "crawler-PROXY_URL配置-058",
  "domain": "crawler",
  "source": "knowledge/crawler/13-project-streamlining-strategy.md",
  "q": "PROXY_URL 配置模式的设计要点？",
  "a": "config 文件中定义默认值，同时支持 HTTPS_PROXY 环境变量覆盖，PROXY_URL 为空时自动跳过代理。代理对浏览器所有请求（页面+API）生效，不影响无代理运行。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: PROXY_URL 配置模式的设计要点？

**A**: config 文件中定义默认值，同时支持 HTTPS_PROXY 环境变量覆盖，PROXY_URL 为空时自动跳过代理。代理对浏览器所有请求（页面+API）生效，不影响无代理运行。
