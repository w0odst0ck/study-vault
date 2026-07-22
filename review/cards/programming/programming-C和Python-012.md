---
{
  "id": "programming-C和Python-012",
  "domain": "programming",
  "source": "knowledge/programming/02-phase-zero-project-startup.md",
  "q": "C++ 和 Python 项目启动时的关键差异？",
  "a": "C++ 需要 CMakeLists.txt/Makefile 构建系统配置 + 头文件路径管理；Python 只需要 requirements.txt/pyproject.toml，\n  无编译步骤。Phase 0 的成本优化策略在 C++ 中对应增量编译（ccache）而非 API 调用控制",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ 和 Python 项目启动时的关键差异？

**A**: C++ 需要 CMakeLists.txt/Makefile 构建系统配置 + 头文件路径管理；Python 只需要 requirements.txt/pyproject.toml，
  无编译步骤。Phase 0 的成本优化策略在 C++ 中对应增量编译（ccache）而非 API 调用控制
