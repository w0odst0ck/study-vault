# 🎋 study-vault

活的知识库。为项目提供知识支持 + 复盘沉淀，逐步积累为个人技术栈。

> 隐私内容（plan/、memory/、knowledge/ 等）仅存本地，不提交。

## 结构

```
study-vault/
├── plan/               ← 各领域学习规划 + 进度跟踪（本地）
├── knowledge/          ← 知识文档（本地）
├── memory/             ← 每日复盘存档（本地）
├── review/             ← SM-2 复习卡片池（本地）
├── references/         ← 跨领域参考资源（本地）
├── project-refs/       ← 项目参考页（本地）
└── scripts/            ← 辅助脚本
    └── review.py       ← 复习引擎
```

## 脚本

### review.py — 间隔重复复习引擎

基于 SM-2 算法，自动从知识文档提取 QA 复习卡片，支持交互式复习与调度。

```bash
python scripts/review.py                # 复习到期卡片
python scripts/review.py import         # 从 knowledge/ 提取 QA → 卡片
python scripts/review.py --quick        # 速刷 5 张
python scripts/review.py --domain rag   # 指定领域
python scripts/review.py stats          # 查看统计
```

使用流程：

1. 在 `knowledge/` 下写知识文档，文末加 `## 回顾` 段落含 Q&A
2. `python scripts/review.py import` → 自动抽取为复习卡片
3. 每天 `python scripts/review.py` → 到期卡片交互式复习 → SM-2 调度下次
4. 复习记录自动写入 `memory/`

### 系统要求

- Python 3.7+
- 标准库（无第三方依赖）
