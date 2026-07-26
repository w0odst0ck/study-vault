---
{
  "id": "crawler-ZKH搜索API路-055",
  "domain": "crawler",
  "source": "knowledge/crawler/12-zkh-waf-bypass.md",
  "q": "ZKH 搜索 API 路径探测的策略和结果？",
  "a": "探测到 `/servezkhApi/product/search` 返回 401（存在但需认证），其他路径返回 404。真实搜索 API 需通过 Playwright 请求拦截捕获（在 Windows 桌面环境运行 probe_api_v2.py），跑通后记录参数格式，迁移回 WSL 模拟调用。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: ZKH 搜索 API 路径探测的策略和结果？

**A**: 探测到 `/servezkhApi/product/search` 返回 401（存在但需认证），其他路径返回 404。真实搜索 API 需通过 Playwright 请求拦截捕获（在 Windows 桌面环境运行 probe_api_v2.py），跑通后记录参数格式，迁移回 WSL 模拟调用。
