#!/usr/bin/env python3
"""
study-vault 飞书同步入口
------------------------
由 Agent 在收到飞书 webhook 消息后调用：
  1. 解析 JSON 中的卡片数据
  2. 合并到 review/cards/
  3. 运行 review.py export 更新 cards.json
  4. git commit + push → 触发 Pages 部署

用法:
    python3 scripts/apply-sync.py        # 合并 sync-results.json（如果有）
    python3 scripts/review.py export     # 导出 cards.json
    # 然后手动 git push

如果 sync-results.json 存在于项目根目录（手动放置），直接运行 apply-sync.py 即可。
"""

import json
import sys
import os
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

# 飞书 webhook 消息中附带的数据格式：
# {
#   "cards": { "card_id": { "interval": 1, "ease": 2.5, "next_review": "2026-07-25", "last_reviewed": "2026-07-24" } },
#   "synced": "2026-07-24T..."
# }

def process(data: dict) -> int:
    """
    将飞书 webhook 数据写入 review/sync-results.json，
    然后执行 apply-sync.py → review.py export
    """
    if not data or "cards" not in data:
        print("数据格式错误：缺少 cards 字段")
        return 1

    # 写入 sync-results.json
    sync_file = BASE / "review" / "sync-results.json"
    sync_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"写入 {sync_file} 共 {len(data['cards'])} 张卡片")

    # 执行 apply-sync.py
    os.chdir(BASE)
    ret = os.system(f"{sys.executable} scripts/apply-sync.py")
    if ret != 0:
        print("apply-sync.py 执行失败")
        return 1

    # 执行 review.py export
    ret = os.system(f"{sys.executable} scripts/review.py export")
    if ret != 0:
        print("review.py export 执行失败")
        return 1

    # 检查是否有变更
    ret = os.system("git diff --quiet -- review/cards/ site/data/")
    if ret == 0:
        print("无变更，跳过提交")
        return 0

    # git commit + push
    os.system("git add review/cards/ site/data/")
    os.system(f'git commit -m "sync: {len(data["cards"])} 张卡片 via 飞书"')
    os.system("git push origin main")
    print(f"已推送 {len(data['cards'])} 张卡片到 main")

    return 0


if __name__ == "__main__":
    # 从 stdin 读取 JSON（飞书 webhook 消息）
    if not sys.stdin.isatty():
        data = json.loads(sys.stdin.read())
    else:
        # 无 stdin 输入时，尝试读取 review/sync-results.json
        sync_file = BASE / "review" / "sync-results.json"
        if sync_file.exists():
            data = json.loads(sync_file.read_text(encoding="utf-8"))
        else:
            print("用法：echo '{\"cards\":...}' | python3 scripts/feishu-sync.py")
            sys.exit(1)

    sys.exit(process(data))
