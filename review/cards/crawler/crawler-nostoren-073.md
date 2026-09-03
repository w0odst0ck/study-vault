---
{
  "id": "crawler-nostoren-073",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "no-store / no-cache / 无指令 三者的缓存行为差异？",
  "a": "- 递进：**存都不存（no-store）/ 存了每次验（no-cache）/ 存了放心用旧的（无指令=启发式缓存）**\n  - no-cache = 可存储但每次使用前必须回源验证（RFC 9111 §5.2.1.4）——不是\"不缓存\"也不是\"保持默认\"",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: no-store / no-cache / 无指令 三者的缓存行为差异？

**A**: - 递进：**存都不存（no-store）/ 存了每次验（no-cache）/ 存了放心用旧的（无指令=启发式缓存）**
  - no-cache = 可存储但每次使用前必须回源验证（RFC 9111 §5.2.1.4）——不是"不缓存"也不是"保持默认"
