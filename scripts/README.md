# 📁 scripts/

知识库辅助脚本。

## 当前脚本

| 脚本 | 说明 |
|------|------|
| `review.py` | SM-2 间隔重复复习引擎 |

### review.py

复习引擎，支持自动卡片提取、交互式复习、统计追踪。

```
python scripts/review.py                # 复习到期卡片
python scripts/review.py import         # 从 knowledge/ 提取 QA → 卡片
python scripts/review.py --quick        # 快速 5 张
python scripts/review.py --domain rag   # 指定领域
python scripts/review.py stats          # 统计
```

详情见 [plan/REVIEW.md](../plan/REVIEW.md)。
