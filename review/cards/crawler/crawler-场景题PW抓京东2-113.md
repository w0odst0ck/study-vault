---
{
  "id": "crawler-场景题PW抓京东2-113",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "场景题：PW 抓京东 200 商品后弹滑块。先怎么鉴别？怎么修？修完怎么确认？",
  "a": "- **鉴别先行**：200 商品后才弹滑块 → 先分**指纹 vs 频率**（固定页数后弹更像频率；体检全绿还弹 → 降频/换 IP）\n  - 验证：过检测页（bot.sannysoft.com 类）体检——webdriver / UA-platform / Canvas 噪声 / WebGL 渲染器 / 字体数 / 时区语言 / 屏幕\n  - 修复：全维度伪装 ① 覆盖 navigator.webdriver（CDP 注入/stealth）② 修 Canvas/WebGL 噪声与渲染器 ③ 字体补全 ④ 时区/语言/屏幕与 UA 一致 → **复检闭环：红了再修直到全绿**",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 场景题：PW 抓京东 200 商品后弹滑块。先怎么鉴别？怎么修？修完怎么确认？

**A**: - **鉴别先行**：200 商品后才弹滑块 → 先分**指纹 vs 频率**（固定页数后弹更像频率；体检全绿还弹 → 降频/换 IP）
  - 验证：过检测页（bot.sannysoft.com 类）体检——webdriver / UA-platform / Canvas 噪声 / WebGL 渲染器 / 字体数 / 时区语言 / 屏幕
  - 修复：全维度伪装 ① 覆盖 navigator.webdriver（CDP 注入/stealth）② 修 Canvas/WebGL 噪声与渲染器 ③ 字体补全 ④ 时区/语言/屏幕与 UA 一致 → **复检闭环：红了再修直到全绿**
