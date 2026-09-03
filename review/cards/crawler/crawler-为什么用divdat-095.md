---
{
  "id": "crawler-为什么用divdat-095",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "为什么用 div[data-sku] 锚定而不是类名？data-sku 改版成 data-skuid 怎么改？",
  "a": "- 数据锚点 vs 视觉类名：**数据必须真实**（无 ID 商品无法标识/下单），视觉可随便改 → data-sku 比类名稳\n  - 结构不可控 → 放弃结构定位，转**文本级正则扫兜底**（价格扫整卡）\n  - 改版应对三件套：① 改**锚定选择器字符串**（不是函数参数）② **检测特征同步**（isJDProductPage）③ **双锚定降级** `div[data-sku], div[data-skuid]`（新旧混存都中）+ 终极防线：抠 script JSON 不依赖属性名",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 为什么用 div[data-sku] 锚定而不是类名？data-sku 改版成 data-skuid 怎么改？

**A**: - 数据锚点 vs 视觉类名：**数据必须真实**（无 ID 商品无法标识/下单），视觉可随便改 → data-sku 比类名稳
  - 结构不可控 → 放弃结构定位，转**文本级正则扫兜底**（价格扫整卡）
  - 改版应对三件套：① 改**锚定选择器字符串**（不是函数参数）② **检测特征同步**（isJDProductPage）③ **双锚定降级** `div[data-sku], div[data-skuid]`（新旧混存都中）+ 终极防线：抠 script JSON 不依赖属性名
