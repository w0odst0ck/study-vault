# 🎋 study-vault

活的知识库骨架。为项目提供知识支持 + 复盘沉淀。

> **隐私说明：** 本仓库为公开骨架仓库，仅包含脚本和前端的项目骨架。
> 知识文档、复习记录、学习规划、参考资源等私有内容保存在本地，不提交到公开仓库。

## 公开内容

```
study-vault/
├── index.md       ← 领域总纲（指引本地目录结构）
├── scripts/       ← 辅助脚本
│   ├── review.py  ← 间隔重复复习引擎（SM-2）
│   ├── annotate.py← 注释系统
│   └── dashboard.py← 知识库仪表盘
├── site/          ← 复习小站前端
│   ├── review/    ← 纯前端 SM-2 复习应用
│   └── index.html ← 仪表盘
└── .github/       ← CI/CD 工作流
```

## 本地私有内容（不上传）

```
├── knowledge/     ← 知识文档（13 领域）
├── memory/        ← 每日复盘日志
├── plan/          ← 学习规划 + 进度跟踪
├── review/        ← 复习卡片池 + 统计
├── annotations/   ← 注释及引文
├── references/    ← 参考资源
├── glossary/      ← 术语表
└── project-refs/  ← 项目参考页
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

### 系统要求

- Python 3.7+
- 标准库（无第三方依赖）
