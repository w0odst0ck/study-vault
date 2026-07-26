---
{
  "id": "crawler-WAF移除脚本执行后为-060",
  "domain": "crawler",
  "source": "knowledge/crawler/13-project-streamlining-strategy.md",
  "q": "WAF 移除脚本执行后为什么需要额外处理 Ant Design 弹窗？",
  "a": "WAF 移除脚本成功执行后，Ant Design Modal（弹窗）可能仍处于打开状态，阻挡后续操作。需要在脚本末尾增加 `document.querySelectorAll('.ant-modal-close').forEach(el => el.click())` 关闭所有弹窗。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: WAF 移除脚本执行后为什么需要额外处理 Ant Design 弹窗？

**A**: WAF 移除脚本成功执行后，Ant Design Modal（弹窗）可能仍处于打开状态，阻挡后续操作。需要在脚本末尾增加 `document.querySelectorAll('.ant-modal-close').forEach(el => el.click())` 关闭所有弹窗。
