# 🎋 study-vault

> 🔗 **在线访问**：[w0odst0ck.github.io/study-vault](https://w0odst0ck.github.io/study-vault/)

个人知识库。写文档 → 自动生成复习卡 → 间隔重复 → 在线阅读。

## 功能

| 页面 | 说明 |
|------|------|
| 📊 **仪表盘** | 卡片统计、复习进度、快速入口 |
| 📇 **复习** | SM-2 间隔重复，键盘操作（空格翻答案，0-5 评分）|
| 📚 **知识库** | 目录树 + Markdown 阅读 + 全文搜索 + 注释侧栏 |
| 📖 **术语表** | 术语浏览 + 搜索筛选 |
| 🔗 **参考资源** | 书籍、课程、工具、数据集索引 |

## 结构

```
study-vault/
├── scripts/         ← 工具脚本
│   ├── review.py    ← 复习引擎 + 数据导出
│   └── serve.py     ← 本地服务
├── site/            ← 前端
│   ├── index.html   ← 仪表盘
│   ├── knowledge/   ← 知识库阅读器
│   ├── review/      ← 复习页
│   ├── glossary/    ← 术语表
│   ├── references/  ← 参考资源
│   └── data/        ← 导出数据（自动生成）
├── knowledge/       ← 知识文档
├── review/          ← 复习卡片
├── annotations/     ← 注释
├── glossary/        ← 术语
└── references/      ← 资源索引
```

## 工作流

### 写知识

```bash
vim knowledge/<domain>/<topic>.md         # 写一篇知识文档
python3 scripts/review.py import          # 从文档提取复习卡片
```

### 复习

```bash
python3 scripts/review.py                 # 复习到期卡片
python3 scripts/review.py --quick         # 速刷 5 张
python3 scripts/review.py --domain xxx    # 指定领域
python3 scripts/review.py stats           # 查看统计
```

### 发布

```bash
python3 scripts/review.py export          # 生成前端数据
python3 scripts/review.py deploy          # 导出 + 提交 + 推送到 GitHub Pages
```

### 本地预览

```bash
python3 scripts/serve.py                  # http://localhost:8080
```

## 卡片管理

复习卡片自动从知识文档的 `## 回顾` 段落提取，SM-2 算法调度：

- 评分 0-2：遗忘 → 重置间隔为 1 天
- 评分 3-5：记住 → 间隔指数增长
- 每日到期卡片自动弹出，完成后结果可下载

## 环境要求

- Python 3.7+
- 标准库（无第三方依赖）

## 在线访问

[打开 study-vault →](https://w0odst0ck.github.io/study-vault/)
