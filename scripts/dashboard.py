#!/usr/bin/env python3
"""
[ 仪表盘 ] 自动生成 index.md 顶部状态卡

用法:
    python scripts/dashboard.py          -> 打印仪表盘
    python scripts/dashboard.py update   -> 写入 index.md
"""

import os
import sys
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8")

import json
import re
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
KNOWLEDGE = BASE / "knowledge"
ANNOTATIONS = BASE / "annotations"
GLOSSARY = BASE / "glossary"
REVIEW = BASE / "review"
STATS_FILE = REVIEW / "stats.json"
INDEX_FILE = BASE / "index.md"

DASHBOARD_MARKER_START = "<!-- DASHBOARD_START -->"
DASHBOARD_MARKER_END = "<!-- DASHBOARD_END -->"


def count_md_files(directory):
    """统计非模板、非 .gitkeep 的 .md 文件数"""
    return len([p for p in directory.rglob("*.md")
                if not p.name.startswith("_") and p.name != ".gitkeep"])


def count_annotations_with_markers():
    """统计带 [ⓘ] 标记的知识文档数"""
    count = 0
    for doc in KNOWLEDGE.rglob("*.md"):
        if doc.name.startswith("_") or doc.name == ".gitkeep":
            continue
        text = doc.read_text(encoding="utf-8")
        if "[ⓘ]" in text:
            count += 1
    return count


def count_docs_by_domain():
    """各领域的文档数 + 对应注释数 + 卡数"""
    domains = defaultdict(lambda: {"docs": 0, "anns": 0, "cards": 0, "name": ""})

    for doc in sorted(KNOWLEDGE.rglob("*.md")):
        if doc.name.startswith("_") or doc.name == ".gitkeep":
            continue
        try:
            rel = doc.relative_to(KNOWLEDGE)
            domain = rel.parts[0]
        except ValueError:
            continue
        domains[domain]["docs"] += 1
        domains[domain]["name"] = doc.read_text(encoding="utf-8").split("\n")[0].lstrip("# ")

    for ann in sorted(ANNOTATIONS.rglob("*.md")):
        if ann.name.startswith("_") or ann.name == ".gitkeep":
            continue
        try:
            rel = ann.relative_to(ANNOTATIONS)
            domain = rel.parts[0]
        except ValueError:
            continue
        domains[domain]["anns"] += 1

    from pathlib import Path as P
    review_cards = REVIEW / "cards"
    for card in review_cards.rglob("*.md"):
        if card.name.startswith("_") or card.name == ".gitkeep":
            continue
        domain = card.parent.name
        domains[domain]["cards"] += 1

    return domains


def generate_dashboard():
    """生成仪表盘 Markdown 块"""
    stats = {}
    if STATS_FILE.exists():
        stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))

    total_cards = stats.get("totalCards", 0)
    due_today = stats.get("dueToday", 0)
    streak = stats.get("streak", 0)
    retention = stats.get("retentionRate", 0.0)

    docs_count = count_md_files(KNOWLEDGE)
    anns_count = count_md_files(ANNOTATIONS)
    gloss_count = count_md_files(GLOSSARY)
    marked_count = count_annotations_with_markers()
    domains = count_docs_by_domain()

    today = date.today().isoformat()

    lines = []
    lines.append(DASHBOARD_MARKER_START)
    lines.append("")
    lines.append("## 📊 知识库状态")
    lines.append("")
    lines.append(f"> 更新于 {today}")
    lines.append("")
    lines.append("```")
    lines.append(f"  知识文档    {docs_count:>3} 篇    复习卡片    {total_cards:>3} 张")
    lines.append(f"  注释文件    {anns_count:>3} 篇    今日到期    {due_today:>3} 张")
    lines.append(f"  术语表      {gloss_count:>2} 个     连续天数    {streak} 🔥")
    lines.append(f"  已标记 [ⓘ] {marked_count:>3} 篇    留存率      {retention}%")
    lines.append("```")
    lines.append("")
    lines.append("| 领域 | 知识 | 注释 | 卡片 |")
    lines.append("|------|------|------|------|")

    # 只显示有内容的领域
    for domain in sorted(domains.keys()):
        info = domains[domain]
        if info["docs"] > 0:
            lines.append(f"| {domain} | {info['docs']}篇 | {info['anns']}篇 | {info['cards']}张 |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(DASHBOARD_MARKER_END)

    return "\n".join(lines)


def cmd_update():
    """将仪表盘写入 index.md"""
    dashboard = generate_dashboard()

    if not INDEX_FILE.exists():
        print(f"❌ {INDEX_FILE} 不存在")
        return

    text = INDEX_FILE.read_text(encoding="utf-8")

    start_pos = text.find(DASHBOARD_MARKER_START)
    end_pos = text.find(DASHBOARD_MARKER_END)

    if start_pos >= 0 and end_pos >= 0:
        # 替换现有仪表盘区域
        end_pos += len(DASHBOARD_MARKER_END)
        new_text = text[:start_pos] + dashboard + text[end_pos:]
    else:
        # 在第一个 --- 后插入
        first_hr = text.find("\n---\n")
        if first_hr >= 0:
            insert_at = first_hr + 5  # 后插
            new_text = text[:insert_at] + "\n" + dashboard + "\n" + text[insert_at:]
        else:
            print("❌ 找不到插入位置")
            return

    INDEX_FILE.write_text(new_text, encoding="utf-8")
    print(f"✅ 仪表盘已更新到 {INDEX_FILE.name}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="📊 知识库仪表盘")
    parser.add_argument("command", nargs="?", default="print",
                        choices=["print", "update"])
    args = parser.parse_args()

    os.chdir(BASE)
    if args.command == "update":
        cmd_update()
    else:
        print(generate_dashboard())


if __name__ == "__main__":
    main()
