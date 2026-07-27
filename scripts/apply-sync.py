#!/usr/bin/env python3
"""
将 web 端同步的复习结果合并到本地卡片文件

用法:
    python3 scripts/apply-sync.py

在 deploy workflow 中运行：
    读取 review/sync-results.json（如果存在），
    更新 review/cards/ 中对应卡片的 SM-2 元数据，
    由调用方（feishu-process.sh）负责删除同步文件。
"""

import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent  # study-vault/
SYNC_FILE = BASE / "review" / "sync-results.json"
CARDS_DIR = BASE / "review" / "cards"


def parse_frontmatter(text):
    """解析 Markdown 文件的 JSON frontmatter，返回 (meta_dict, body)"""
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return None, None
    try:
        return json.loads(m.group(1)), m.group(2).strip()
    except json.JSONDecodeError:
        return None, None


def write_frontmatter(filepath, meta, body):
    """写回 frontmatter + body 到 Markdown 文件"""
    content = f"---\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n---\n\n{body}\n"
    filepath.write_text(content, encoding="utf-8")


def main():
    if not SYNC_FILE.exists():
        print("📭 没有待处理的同步数据")
        return

    sync = json.loads(SYNC_FILE.read_text(encoding="utf-8"))
    cards_data = sync.get("cards", {})
    if not cards_data:
        print("⚠️ 同步文件为空")
        return

    # 建立 cardId → (文件路径, meta字典, body文本) 的映射
    card_map = {}
    for f in CARDS_DIR.rglob("*.md"):
        if f.name.startswith("_"):
            continue
        try:
            meta, body = parse_frontmatter(f.read_text(encoding="utf-8"))
            if not meta:
                continue
            cid = meta.get("id") or meta.get("card_id")
            if cid:
                card_map[cid] = (f, meta, body)
        except (json.JSONDecodeError, KeyError):
            continue

    updated = 0
    not_found = 0

    for cid, new_state in cards_data.items():
        if cid in card_map:
            fpath, meta, body = card_map[cid]
            meta["interval"] = new_state.get("interval", meta.get("interval", 0))
            meta["ease"] = new_state.get("ease", meta.get("ease", 2.5))
            meta["next_review"] = new_state.get("next_review",
                                                 meta.get("next_review", ""))
            meta["last_reviewed"] = new_state.get("last_reviewed",
                                                   meta.get("last_reviewed", ""))
            # reviews: webhook 传了就用 web 端的值，否则本地 +1
            if "reviews" in new_state:
                meta["reviews"] = new_state["reviews"]
            else:
                meta["reviews"] = meta.get("reviews", 0) + 1

            write_frontmatter(fpath, meta, body)
            updated += 1
        else:
            not_found += 1

    print(f"✅ 已同步 {updated} 张卡片")
    if not_found:
        print(f"⚠️  {not_found} 张卡片未找到（可能已删除）")


if __name__ == "__main__":
    main()
