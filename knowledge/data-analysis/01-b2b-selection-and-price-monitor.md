---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-22",
  "tags": [
    "数据分析",
    "选品分析",
    "价格监控",
    "B2B"
  ],
  "cards": [
    "data-analysis-价格预警的触发条件和冷启-002",
    "data-analysis-品牌提取准确率从0-003",
    "data-analysis-四层选品策略模型各层含义-001"
  ]
}
---

# B2B 选品分析与缺口匹配

> 来源：PH(震坤行选品)、price-compare 项目
> 日期：2026-07

## 选品策略分层

四层策略模型[ⓘ]：

| 层级 | 说明 | 策略 |
|------|------|------|
| 🟢 **必上** | 强需求、高利润 | 立即上架 |
| 🔵 **推荐** | 有潜力的品类 | 优先上架 |
| 🟡 **暗马** | 长尾、竞品覆盖少 | 试探上架 |
| 🔘 **关注** | 趋势待观察 | 先不动 |

## 多平台缺口分析

### 6 步流水线

```python
# gap/ 缺口分析模块
1. 读选品清单（建议上架的商品）
2. 读在售清单（已上架的商品）
3. 标准化键（统一品牌/型号格式）
4. 差集运算（选品 - 在售 = 缺口）
5. 模糊匹配（处理命名差异）
6. 导出 Excel（缺品明细）
```

### 核心逻辑
- **输出**：缺品明细 + 门类/策略统计 + 潜匹配人工确认表
- **数据驱动**：三平台（京东/震坤行/1688）搜索页数据输入

## 价格监控体系

### 架构

```python
monitor/
├── db.py          # SQLite 三层表（商品/快照/预警）
├── ingester.py    # 三平台 CSV → 入库
└── alerter.py     # 预警引擎
```

### 预警方案

- **方法**：移动平均[ⓘ] vs 当前价偏离（非逐次比对）
- **阈值**：偏离 ≥ 10% 触发
- **冷启动[ⓘ]**：快照 < 3 次不出声（避免冷启动误报）
- **输出**：有预警写 CSV+TXT，无预警零噪声

### 数据库设计

```sql
-- 三层表
CREATE TABLE products (     -- 商品层
    id TEXT PRIMARY KEY, brand TEXT, model TEXT, platform TEXT
);
CREATE TABLE snapshots (    -- 快照层
    id INTEGER PK, product_id TEXT FK, price REAL, captured_at TIMESTAMP
);
CREATE TABLE alerts (       -- 预警层
    id INTEGER PK, product_id TEXT FK, deviation REAL, triggered_at TIMESTAMP
);
```

## B2B 工业品平台特点

- **搜索引擎**：京东搜索京东 industrial.jd.com 已废弃，转向 SPA 架构
- **1688**：采购助手插件 XLSX 导出为主力数据源
- **震坤行**：WAF + Cloudflare 双重保护，SSR 数据提取
- **选品模板**：统一 `selection_schema.py`，每品类 10 条推荐

## 产品方向决策

- ❌ Streamlit[ⓘ]（原型验证后废弃）
- ❌ gap/ 缺口分析模块（单独产品化价值低）
- ❌ Tauri 桌面端（开发成本高）
- ✅ **Flask Web**（主力路线）

## 价格提取技巧

### 品牌提取
```python
# 标题+店铺双重解析[ⓘ] → 品牌提取准确率 0%→91%
def extract_brand(title: str, shop_name: str) -> str:
    # 从标题中匹配已知品牌列表
    # 从店铺名中提取品牌信息
    # 两者交叉验证
```

### 1688 详情页
- CDN 直链 `cbu01.alicdn.com`
- SingleFile 保存图片：`data-sf-original-src` → CDN 直链
- Ctrl+S `_files/` 目录兜底

## 回顾
<!-- cards: data-analysis-价格预警的触发条件和冷启-002, data-analysis-品牌提取准确率从0-003, data-analysis-四层选品策略模型各层含义-001 -->
<!-- cards: data-analysis-价格预警的触发条件和冷启-002, data-analysis-品牌提取准确率从0-003, data-analysis-四层选品策略模型各层含义-001 -->
- Q: 四层选品策略模型各层含义是什么？
  A: 🟢必上（强需求高利润）→立即上架、🔵推荐（有潜力）→优先上架、🟡暗马（长尾竞品覆盖少）→试探上架、🔘关注（趋势待观察）→先不动。
- Q: 价格预警的触发条件和冷启动规则是什么？
  A: 移动平均 vs 当前价偏离 ≥10% 触发预警；快照不足 3 次时不预警，避免冷启动误报。无预警时零噪声输出。
- Q: 品牌提取准确率从 0% 提升到 91% 的关键方法是什么？
  A: 双重解析策略——从标题中匹配已知品牌列表 + 从店铺名中提取品牌信息，两者交叉验证。
