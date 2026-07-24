# 🔧 工具链

> 知识库中实际使用的工具、库、框架索引

---

## 浏览器自动化

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [Playwright](https://playwright.dev/) | 浏览器自动化（Chromium/Firefox/WebKit） | 爬虫系列 | 主力爬虫工具，比 Selenium API 更现代 |
| [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/) | PDF 文字提取 | `crawler/04` | 最快：0.12s/59页 |
| [pymupdf4llm](https://github.com/pymupdf/pymupdf4llm) | PDF→Markdown（含表格） | `crawler/04` | 基于 PyMuPDF，适合 LLM 输入 |
| [pdfplumber](https://github.com/jsvine/pdfplumber) | PDF 文本+表格提取 | `crawler/04` | 备选，比 PyMuPDF 慢但提取更精细 |

## OCR

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) | 开源 OCR 引擎 | `crawler/04` | 需 `sudo` 系统安装，中文包 `chi_sim` |
| [EasyOCR](https://github.com/JaidedAI/EasyOCR) | 纯 pip 安装的 OCR | `crawler/04` | 含 PyTorch ~500MB，未实测 |

## 数据建模 & 验证

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [Pydantic v2](https://docs.pydantic.dev/) | Python 数据验证 | `programming/01` | `BaseModel` + `model_validator` |
| [Jinja2](https://jinja.palletsprojects.com/) | Python 模板引擎 | `programming/02` | 生成笔记模板 |

## Web 框架

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [Flask](https://flask.palletsprojects.com/) | Python Web 框架 | `data-analysis/01` | 主力路线 |
| [Streamlit](https://streamlit.io/) | 数据原型工具 | `data-analysis/01` | 原型验证后废弃 |

## 数据库

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [SQLite FTS5](https://www.sqlite.org/fts5.html) | 全文搜索引擎 | `crawler/03` | 零配置，中文需 `unicode61` tokenizer |

## 开发工具

| 工具 | 用途 | 知识文档 | 备注 |
|------|------|---------|------|
| [GitHub REST API](https://docs.github.com/en/rest) | Star 仓库管理 | `programming/02` | 需 `star+json` header |
| [pandas](https://pandas.pydata.org/) | 数据分析 | `data-analysis/01` | B2B 选品分析主力 |
| [Click](https://click.palletsprojects.com/) | Python CLI 框架 | 多项目 | CLI 入口 |
| [httpx](https://www.python-httpx.org/) | HTTP 客户端 | 多项目 | 比 requests 更现代 |
