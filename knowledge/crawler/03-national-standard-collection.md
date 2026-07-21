---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-21",
  "tags": [
    "爬虫",
    "国家标准",
    "数据采集"
  ],
  "cards": [
    "crawler-SAMR平台的速率限制-013",
    "crawler-openstd的PD-015",
    "crawler-中国照明国标中约多少比例-014",
    "crawler-爬虫架构中新增一个数据源-012"
  ]
}
---

# 国家标准信息采集实战

> 来源：BriefNexus 项目 standards/ 模块
> 日期：2026-07

## 数据源一览

| 平台 | 状态 | 说明 |
|------|------|------|
| **SAMR（全国标准信息公共服务平台）** | ✅ 稳定 | 搜索API + 详情页可用 |
| **openstd（标准全文公开）** | ❌ 已死 | PDF下载通道已关闭 |
| **bzxz.net（标准下载网）** | ⚠️ 部分有效 | 详情页正文可抓，PDF已失效 |
| **SPC（标准在线服务网）** | ❌ 不可达 | API返回系统异常 |
| **CSRES（工标网）** | ⏸ 待验证 | 默认关闭 |
| **IEC Webstore** | ⚠️ JS渲染 | 需 publication_id 才能抓取 |
| **其他分享站** | 💰 需付费 | bzgfw/准行天下/书客网 |

## SAMR API 接口

```bash
# 搜索列表
GET /gb/search/gbQueryPage?searchText=KEYWORD&ics=&state=&ISSUE_DATE=&pageNumber=N&pageSize=S

# 响应结构
{ total, pageNumber, rows: [{id, C_C_NAME, C_STD_CODE, STD_NATURE, STATE, ISSUE_DATE, ...}] }

# ICS代码提取：从详情页 <td> 解析 "29.140.40 照明设备" 格式
```

### 速率限制
```
X-RateLimit-Remaining: 196     # 剩余配额
X-RateLimit-Burst-Capacity: 200  # 突发容量
X-RateLimit-Replenish-Rate: 80   # 补充速率
```

## openstd PDF 下载流程（已失效）

曾经有效但现已不可用的 3 步 Session 流程：

```python
# Step 1: 访问详情页建立 session
session.get(f"/bzgk/std/newGbInfo?hcno={hcno}")
# Step 2: 触发服务端校验
session.get(f"/bzgk/std/showGb?type=download&hcno={hcno}")
# Step 3: 获取 PDF 流
session.get(f"/bzgk/std/viewGb?hcno={hcno}")
```

失败原因：showGb 端点 404 → `/WEB-INF/404.jsp`，viewGb 空响应（API 变动/权限变更）

## 爬虫架构：适配器[ⓘ] + 配置驱动

### 模块设计

```python
crawler/
├── main.py                  # CLI 入口
├── utils.py                 # HTTP工具、标准化、去重
├── platforms/               # 平台适配器（可插拔）
│   ├── base.py              # BaseCollector 基类
│   ├── samr.py              # SAMR 采集器
│   ├── spc.py               # SPC 采集器（已禁用）
│   ├── openstd.py           # openstd 采集器
│   └── iec.py               # IEC 采集器
└── downloader.py            # 下载管理器
```

### 配置驱动扩展[ⓘ]

```ini
# standards_config.ini
[crawler]
enable_samr = true
enable_spc = false
enable_csres = false
```

**新增数据源只需写适配器 + 注册配置，引擎代码零修改。**

## SQLite FTS5[ⓘ] 全文搜索

```sql
-- 主表
CREATE TABLE standards (
    std_code TEXT PRIMARY KEY,
    title TEXT, category TEXT, state TEXT,
    issue_date TEXT, local_path TEXT,
    is_adopted INTEGER, intl_source TEXT
);

-- FTS5 全文索引（含中文分词回退）
CREATE VIRTUAL TABLE standards_fts USING fts5(
    title, std_code, content='standards', content_rowid='rowid',
    tokenize='unicode61'
);
```

- 双引擎搜索：FTS5 全文搜索 → LIKE 中文回退
- ICS 分类树浏览：根 → 子节点 → 标准列表
- JSON 输出供 pandas 消费

## 采标[ⓘ]映射（IEC/CIE/CISPR）

设计一条知识：约 76% 的中国照明国标是**采标**（adopted from IEC/CIE 国际标准）

```python
# GB/T 标准号 → 国际源 映射
intl_mappings = {
    "7000": "IEC 60598",      # 灯具系列
    "19510": "IEC 61347",     # 灯的控制装置
    "30104": "IEC 62031",     # LED 模块
    "32483": "IEC 62717",     # LED 灯具性能
}
```

结果：355 条照明标准，270 条采标（IEC=225, CIE=13, CISPR=1），85 条国内自主

## 教训

1. **免费 PDF 下载通道不可靠[ⓘ]** — openstd 随时会关，bzxz.net 链接会过期
2. **先分类再下载** — 采标（有国际源）国内不提供公开全文概率极大
3. **IP 限流要预留冷却时间** — 全量冲容易封 IP
4. **WSL2 下的 Playwright 有限制** — headed 模式需要 X Server
5. **替代源探测要快速验证** — 各个分享站逐一试，不行就放弃

## 回顾
<!-- cards: crawler-SAMR平台的速率限制-013, crawler-openstd的PD-015, crawler-中国照明国标中约多少比例-014, crawler-爬虫架构中新增一个数据源-012 -->
<!-- cards: crawler-SAMR平台的速率限制-013, crawler-openstd的PD-015, crawler-中国照明国标中约多少比例-014, crawler-爬虫架构中新增一个数据源-012 -->
<!-- cards: crawler-SAMR平台的速率限制-013, crawler-openstd的PD-015, crawler-中国照明国标中约多少比例-014, crawler-爬虫架构中新增一个数据源-012 -->
- Q: 爬虫架构中新增一个数据源需要改哪些代码？
  A: 只需写适配器类（继承 `BaseCollector`）+ 在 `standards_config.ini` 注册配置，引擎代码零修改。
- Q: SAMR 平台的速率限制参数有哪些？
  A: `X-RateLimit-Remaining`（剩余配额）、`X-RateLimit-Burst-Capacity`（突发容量 200）、`X-RateLimit-Replenish-Rate`（补充速率 80）。
- Q: 中国照明国标中约多少比例是采标？主要来源是什么？
  A: 约 76%（355 条照明标准中 270 条采标），主要来源 IEC（225 条）、CIE（13 条）、CISPR（1 条）。
- Q: openstd 的 PDF 下载通道为什么不可用？
  A: showGb 端点返回 404、viewGb 空响应，API 变动或权限变更导致曾经有效的 3 步 Session 流程全部失效。
