---
{
  "id": "programming-配置管理的三层搜索路径优-002",
  "domain": "programming",
  "source": "knowledge/programming/01-pydantic-v2-model-design.md",
  "q": "配置管理的三层搜索路径优先级是什么？",
  "a": "`--config` 命令行指定 > `./star-vault.yaml` 配置文件 > 内置默认值。环境变量进一步覆盖配置值。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: 配置管理的三层搜索路径优先级是什么？

**A**: `--config` 命令行指定 > `./star-vault.yaml` 配置文件 > 内置默认值。环境变量进一步覆盖配置值。
