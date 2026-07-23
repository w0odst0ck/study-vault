#!/usr/bin/env python3
"""
将 web 端同步的复习结果合并到本地卡片文件

用法:
    python3 scripts/apply-sync.py

在 deploy workflow 中运行：
    读取 review/sync-results.json（如果存在），
    更新 review/cards/ 中对应卡片的 SM-2 元数据，
    然后删除同步文件。
"""

import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # study-vault/
SYNC_FILE = BASE / "review" / "sync-results.json"
CARDS_DIR = BASE / "review" / "cards"


def main():
    if not SYNC_FILE.exists():
        print("📭 没有待处理的同步数据")
        return

    sync = json.loads(SYNC_FILE.read_text(encoding="utf-8"))
    cards_data = sync.get("cards", {})
    if not cards_data:
        print("⚠️ 同步文件为空")
        SYNC_FILE.unlink()
        return

    # 建立 cardId → 卡文件路径 的映射
    card_map = {}
    for f in CARDS_DIR.rglob("*.json"):
        try:
            card = json.loads(f.read_text(encoding="utf-8"))
            cid = card.get("meta", {}).get("id") or card.get("meta", {}).get("card_id")
            if cid:
                card_map[cid] = (f, card)
        except (json.JSONDecodeError, KeyError):
            continue

    updated = 0
    not_found = 0

    for cid, new_state in cards_data.items():
        if cid in card_map:
            fpath, card = card_map[cid]
            meta = card["meta"]
            meta["interval"] = new_state.get("interval", meta.get("interval", 0))
            meta["ease"] = new_state.get("ease", meta.get("ease", 2.5))
            meta["next_review"] = new_state.get("next_review",
                                                 meta.get("next_review", ""))
            meta["last_reviewed"] = new_state.get("last_reviewed",
                                                   meta.get("last_reviewed", ""))
            meta["reviews"] = meta.get("reviews", 0) + 1
            fpath.write_text(json.dumps(card, ensure_ascii=False, indent=2),
                             encoding="utf-8")
            updated += 1
        else:
            not_found += 1

    # 清理同步文件
    SYNC_FILE.unlink()

    print(f"✅ 已同步 {updated} 张卡片")
    if not_found:
        print(f"⚠️  {not_found} 张卡片未找到（可能已删除）")


if __name__ == "__main__":
    main()
