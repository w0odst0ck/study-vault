---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-22",
  "tags": [
    "爬虫",
    "PDF",
    "OCR",
    "参数提取"
  ],
  "cards": [
    "crawler-PDF参数页定位器的核-005",
    "crawler-文字层检测和OCR路-006",
    "crawler-编码异常的PDF如何-008",
    "crawler-规则分级的P0P1-007"
  ]
}
---

# PDF 参数页定位器实战

> 来源：BriefNexus 项目 pdf-extract-bench → tools/locator
> 日期：2026-07

## 项目定位转变

**定位优先于提取[ⓘ]**——精确参数提取需要人工确认，但定位参数在哪一页可以自动化，把工作量从"翻 59 页找参数"降到"看 5 页参数页"。

```
传统思路: PDF → Markdown → OCR 自动提取参数值
             ↓  OCR 中文表格精度仅 60-70%，不可靠
实战方案: PDF → 自动定位参数页在哪 → 人工看几页
```

**定位策略**：不追求提取精确参数值，改为参数页定位器 + 人工确认。

## 架构

```
locator/
├── detector.py         ← 统一入口（text / ocr / hybrid / auto 模式）
├── patterns/
│   ├── __init__.py     ← 规则注册
│   ├── lighting.py     ← 照明类规则
│   ├── automotive.py   ← 汽车类规则
│   └── yaml/           ← YAML 配置版规则
├── model_hook.py       ← PageDetector 抽象基类（预留 ML 接入）
└── index.py            ← 汇总产出 index.json
```

`model_hook.py` 预留了 ML 模型接口，未来可替换检测器而不拆架构。

## 测试集（7 份 PDF 覆盖三路线）

| 文件 | 页数 | 路线 | 参数类型 |
|------|------|------|---------|
| GB_4599-2024.pdf | 59 | text | 前照灯配光曲线、照度值 |
| GB_13954-2009.pdf | 18 | text | 警示灯光度参数、色度 |
| GB_19152-2025.pdf | 55 | text | 摩托车配光曲线 |
| GB_4785-2019.pdf | 82 | text | **编码异常**，所有数字提取器乱码 |
| GB_23826-2025.pdf | 35 | hybrid | 文字+扫描混合 |
| GB_T_5700-2023.pdf | 52 | ocr | 照明测量数据表 |
| GB_T_7922-2023.pdf | 17 | ocr | 色度坐标表 |

## 双路线检测

```python
detectors:
  text: TextDetector      # 文字层检测（PDF 内置文字）
  ocr: OcrDetector        # 扫件 OCR 检测（Tesseract[ⓘ]）
  hybrid: HybridDetector  # 融合模式
```

### 文字层路线
- **PyMuPDF[ⓘ]**（最快，0.12s/59 页）
- **pymupdf4llm[ⓘ]** 将 PDF 转 Markdown（含表格，~0.3s，但单元格有碎片）
- `pdfplumber` 作为备选
- 规则匹配：关键词（光通量、色温、显色指数、功率因数...）

### OCR 路线
- **Tesseract 5.5** + `chi_sim` 中文语言包
- **EasyOCR[ⓘ]**（pip 全自动安装，含 PyTorch ~500MB）未实测
- 扫件 PDF 的表格数值精度不足（60-70%）
- 需要 `sudo` 安装 Tesseract 和相关语言包

### 规则分级

| 等级 | 条件 | 示例 |
|------|------|------|
| P0 | 命中 1 个即参数页 | 配光性能、光度参数、测试点 |
| P1 | 命中 3+ 即参数页 | 照度、亮度、色温、cd、lm |
| P2 | 需 P1+P2 组合验证 | 最小值、最大值、公差、限值 |

两条路线（text + OCR）共用同一套关键词规则。

## 规则配置化

```yaml
# yaml/lighting.yaml — 照明标准参数规则
keywords:
  - 光通量
  - 色温
  - 显色指数
  - 功率因数
  - 额定电压
  - 额定功率
  - 光效
  # ...
  
patterns:
  - '\d+[.\d]*\s*lm'    # 流明值
  - '\d{3,4}\s*K'       # 色温
  - 'Ra\s*\d+'           # 显色指数
```

**不碰代码**，新增标准类型只需写对应 YAML 文件。

## 验证工具

```bash
python validate.py --ground-truth gt.yaml --result result.yaml
# 输出: 3 秒出查全率/查准率
```

### 首跑结果
| 标准 | 查全率 | 查准率 | 说明 |
|------|--------|--------|------|
| GB 4599 | 100% | 58.3% | 7/7 参数全部抓到，但有误检 |
| GB 13954 | 0% | — | 编码异常 |
| GB 4785 | 0% | — | 编码异常 |
| GB 19152 | 0% | — | 用词不同，需扩展 lighting.yaml |

## 关键技术点

### 1. 混合检测器
```python
class HybridDetector:
    """文字层优先，OCR 兜底[ⓘ]"""
    def detect(self, pdf_path):
        text_results = text_detector.detect(pdf_path)
        if text_results.confidence > 0.8:
            return text_results
        return ocr_detector.detect(pdf_path, text_results.missed_pages)
```

### 2. 参数页定位
- 不追求精确提取参数值
- 定位参数在哪些页码，输出页码区间
- 人工看几页就能确认

### 3. 缓存机制
- OCR 结果缓存到本地（320 页缓存示例）
- `--mode auto` 自动续跑，跳过已缓存页

## 关键决策

1. **定位器只标记页，不提取值** — 数值精度不足以自动化
2. **两条路线共用规则** — text + OCR 走同一套关键词，降低维护成本
3. **规则分 YAML + Python 双版本** — YAML 方便非开发者配参
4. **model_hook 预留 ML 接口** — 未来换模型不拆架构
5. **Tesseract OCR 环境依赖非 pip 化** — 需系统级安装，部署需确认

## 已知限制

- **Tesseract 系统依赖**：需要 `sudo apt install tesseract-ocr tesseract-ocr-chi-sim`，不可纯 pip 化
- **编码异常 PDF**：GB 4785 类 PDF 所有数字提取器乱码，只能 OCR 捞正文
- **扫描件表格精度**：仅 60-70%，数值不可自动提取
- **规则覆盖率**：当前只覆盖照明类，汽车照明/信号灯等需扩展
- **全量数据集**：108 个 PDF 的 sources.csv 数据源未在仓库中（仅 7 个测试 PDF）

## 待改进

- YAML 规则扩展覆盖更多标准类型（汽车照明、信号灯等）
- Tesseract 中文表格 OCR 精度提升
- 扫件 PDF `sudo` 依赖问题
- 全量 108 个 PDF 批量验证

## 回顾
<!-- cards: crawler-PDF参数页定位器的核-005, crawler-文字层检测和OCR路-006, crawler-编码异常的PDF如何-008, crawler-规则分级的P0P1-007 -->
<!-- cards: crawler-PDF参数页定位器的核-005, crawler-文字层检测和OCR路-006, crawler-编码异常的PDF如何-008, crawler-规则分级的P0P1-007 -->
<!-- cards: crawler-PDF参数页定位器的核-005, crawler-文字层检测和OCR路-006, crawler-编码异常的PDF如何-008, crawler-规则分级的P0P1-007 -->
- Q: PDF 参数页定位器的核心定位策略是什么？
  A: 定位优先于提取——自动化定位参数在哪一页，人工确认精确数值，工作量从"翻 59 页"降到"看 5 页"。
- Q: 文字层检测和 OCR 路线分别用什么工具？
  A: 文字层用 PyMuPDF（最快，0.12s/59 页）或 pymupdf4llm；OCR 用 Tesseract 5.5 + chi_sim。EasyOCR 作为 OCR 替代方案（pip 全自动但含 PyTorch ~500MB）。
- Q: 规则分级的 P0/P1/P2 各是什么条件？
  A: P0 命中 1 个即判参数页（如"配光性能"）、P1 命中 3+ 即判（如"照度""色温"）、P2 需 P1+P2 组合验证（如"最小值""公差"）。
- Q: 编码异常的 PDF 如何应对？
  A: GB 4785 类 PDF 中所有数字提取器乱码，只能通过 OCR 捞取正文信息。
