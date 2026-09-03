---
{
  "id": "crawler-重排vs重绘col-102",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "重排 vs 重绘？color/width 触发哪个？为什么读 offsetWidth 是性能坑？只动 transform/opacity 为什么不触发？",
  "a": "- 重绘 = 改像素（便宜）；重排 = 改尺寸/位置（贵）；color→重绘 / width→重排\n  - 读几何（offsetWidth）→ 此前攒着的样式改动被迫生效 → **强制同步布局**（forced reflow）；先读后写避免反复强迫\n  - transform/opacity：**跳过④布局⑤绘制，直接走合成**（GPU 图层），成本最低",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 重排 vs 重绘？color/width 触发哪个？为什么读 offsetWidth 是性能坑？只动 transform/opacity 为什么不触发？

**A**: - 重绘 = 改像素（便宜）；重排 = 改尺寸/位置（贵）；color→重绘 / width→重排
  - 读几何（offsetWidth）→ 此前攒着的样式改动被迫生效 → **强制同步布局**（forced reflow）；先读后写避免反复强迫
  - transform/opacity：**跳过④布局⑤绘制，直接走合成**（GPU 图层），成本最低
