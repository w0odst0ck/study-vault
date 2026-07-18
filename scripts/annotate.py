#!/usr/bin/env python3
"""
[ 注释管理 ] 检查知识文档 ↔ 注释文件覆盖情况 + 标记缺失

用法:
    python scripts/annotate.py check       -> 检查注释覆盖
    python scripts/annotate.py mark        -> 列出缺 [ⓘ] 标记的文档
    python scripts/annotate.py glossary    -> 列出 glossary 使用情况
"""

import os
import sys
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8")

import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
KNOWLEDGE = BASE / "knowledge"
ANNOTATIONS = BASE / "annotations"
GLOSSARY = BASE / "glossary"


def _rel_knowledge(path):
    """返回 knowledge/ 下的相对路径"""
    try:
        return path.relative_to(KNOWLEDGE)
    except ValueError:
        return path.name


def _rel_annotations(path):
    """返回 annotations/ 下的相对路径"""
    try:
        return path.relative_to(ANNOTATIONS)
    except ValueError:
        return path.name


def cmd_check():
    """检查每篇知识文档是否有对应的注释文件 + [ⓘ] 标记覆盖率"""
    print("\n📋 注释覆盖检查\n")

    total_docs = 0
    has_annotation = 0
    total_markers = 0
    missing_markers = 0
    uncovered_docs = []

    for doc_path in sorted(KNOWLEDGE.rglob("*.md")):
        if doc_path.name.startswith("_") or doc_path.name == ".gitkeep":
            continue

        total_docs += 1
        rel = _rel_knowledge(doc_path)
        ann_path = ANNOTATIONS / rel

        doc_text = doc_path.read_text(encoding="utf-8")
        markers = len(re.findall(r"\[ⓘ\]", doc_text))
        total_markers += markers

        if ann_path.exists():
            has_annotation += 1
            ann_text = ann_path.read_text(encoding="utf-8")
            ann_entries = len(re.findall(r"## L[1-4] \[?\[?`?([^\]\n]+)", ann_text))

            if markers == 0 and ann_entries > 0:
                uncovered_docs.append((rel, "缺 [ⓘ] 标记"))
                missing_markers += 1
            elif markers < ann_entries:
                uncovered_docs.append((rel, f"标记不足（{markers}个[ⓘ] < {ann_entries}条注释）"))
                missing_markers += 1
        else:
            uncovered_docs.append((rel, "无注释文件"))
            missing_markers += 1

    print(f"  知识文档：{total_docs} 篇")
    print(f"  有注释文件：{has_annotation} 篇（{has_annotation/total_docs*100:.0f}%）" if total_docs else "  有注释文件：0 篇")
    print(f"  [ⓘ] 标记总数：{total_markers}")

    if uncovered_docs:
        print(f"\n  ⚠️  需处理：")
        for rel, reason in uncovered_docs:
            print(f"     {reason} → {rel}")

    print(f"\n  glossary 术语数：{len(list(GLOSSARY.rglob('*.md')))} 个")


def cmd_mark():
    """列出 knowledge/ 中哪些文档缺 [ⓘ] 标记"""
    print("\n📝 缺 [ⓘ] 标记的文档\n")

    found = False
    for doc_path in sorted(KNOWLEDGE.rglob("*.md")):
        if doc_path.name.startswith("_") or doc_path.name == ".gitkeep":
            continue
        text = doc_path.read_text(encoding="utf-8")
        if "[ⓘ]" not in text:
            print(f"  ⚠️  {_rel_knowledge(doc_path)}")
            found = True

    if not found:
        print("  全部已标记 ✅")


def cmd_glossary():
    """列出 glossary 术语及其被引用情况"""
    print("\n📖 术语使用情况\n")

    terms = {}
    for g_path in sorted(GLOSSARY.rglob("*.md")):
        if g_path.name.startswith("_") or g_path.name == ".gitkeep":
            continue
        term = g_path.stem
        # 扫描 knowledge + annotations 中的引用
        refs = []
        for scope in [KNOWLEDGE, ANNOTATIONS]:
            for doc in scope.rglob("*.md"):
                if doc.name.startswith("_") or doc.name == ".gitkeep":
                    continue
                text = doc.read_text(encoding="utf-8")
                if f"[[glossary/{term}" in text:
                    try:
                        refs.append(doc.relative_to(BASE))
                    except ValueError:
                        refs.append(str(doc))
        terms[term] = refs

    if not terms:
        print("  📭 glossary 为空")
        return

    for term, refs in sorted(terms.items()):
        if refs:
            print(f"  ✅ {term} — 被 {len(refs)} 处引用")
        else:
            print(f"  ⚠️  {term} — 未被引用")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="📖 注释管理工具")
    parser.add_argument("command", choices=["check", "mark", "glossary"],
                        default="check", nargs="?")
    args = parser.parse_args()

    os.chdir(BASE)
    if args.command == "check":
        cmd_check()
    elif args.command == "mark":
        cmd_mark()
    else:
        cmd_glossary()


if __name__ == "__main__":
    main()
