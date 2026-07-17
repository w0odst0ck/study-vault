#!/usr/bin/env python3
"""
[ 复习引擎 ] SM-2 间隔重复 + 自动卡片提取

用法:
    python scripts/review.py                -> 复习到期的卡片
    python scripts/review.py import         -> 从 knowledge/ 提取卡片
    python scripts/review.py --quick        -> 快速复习 5 张
    python scripts/review.py --domain rag   -> 指定领域
    python scripts/review.py --reset        -> 重置所有卡片间隔
    python scripts/review.py stats          -> 查看统计
"""

import os
import sys
# Windows GBK 兼容
if os.name == "nt":
    sys.stdout.reconfigure(encoding="utf-8")

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

# ── 路径 ──
BASE = Path(__file__).resolve().parent.parent  # study-vault/
KNOWLEDGE = BASE / "knowledge"
REVIEW = BASE / "review"
CARDS = REVIEW / "cards"
STATS_FILE = REVIEW / "stats.json"
LOG_FILE = REVIEW / "_review-log.md"
MEMORY = BASE / "memory"

# ── SM-2 算法 ──


def sm2_next(interval, ease, rating):
    """SM-2 间隔重复调度"""
    if rating < 3:  # 遗忘
        interval = 1
    else:
        if interval == 0:
            interval = 1
        elif interval == 1:
            interval = 6
        else:
            interval = round(interval * ease)
        ease = ease + (0.1 - (5 - rating) * (0.08 + (5 - rating) * 0.02))
        ease = max(1.3, ease)
    next_review = (date.today() + timedelta(days=interval)).isoformat()
    return interval, round(ease, 2), next_review


# ── 卡片 I/O ──


def parse_card(filepath):
    """解析单张卡片文件（JSON front matter）"""
    text = filepath.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return None, None
    meta = json.loads(m.group(1))
    body = m.group(2).strip()
    return meta, body


def write_card(filepath, meta, body):
    """写卡片文件"""
    content = f"---\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n---\n\n{body}\n"
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(content, encoding="utf-8")


def load_all_cards():
    """加载所有卡片"""
    cards = []
    for fpath in sorted(CARDS.rglob("*.md")):
        if fpath.name.startswith("_"):
            continue
        meta, body = parse_card(fpath)
        if meta:
            cards.append((fpath, meta, body))
    return cards


# ── 自动抽取（knowledge/ → review/） ──


def extract_qa_from_doc(filepath):
    """从知识文档中提取 Q&A 对"""
    text = filepath.read_text(encoding="utf-8")
    # 找 ## 回顾 段落
    sections = re.split(r"^##\s+回顾", text, flags=re.MULTILINE)
    if len(sections) < 2:
        return []
    qa_section = sections[1].split("\n## ")[0]  # 取到下一个标题为止

    qas = []
    # 匹配 - Q: ... \n   A: ...
    pattern = re.compile(
        r"^\s*-\s*Q:\s*(.*?)\n\s*A:\s*(.*?)(?=\n\s*-\s*Q:|\n\s*$|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    for m in pattern.finditer(qa_section):
        q = m.group(1).strip()
        a = m.group(2).strip()
        if q and a:
            qas.append((q, a))
    return qas


def generate_card_id(domain, question):
    """从问题和领域生成短 ID"""
    # 取前 4 个中文字/英文词做 ID
    short = re.sub(r"[^\w]", "", question[:12])
    if not short:
        short = str(hash(question))[-6:]
    seq = len(list((CARDS / domain).glob("*.md"))) + 1
    return f"{domain}-{short}-{seq:03d}"


def cmd_import(force=False):
    """扫描 knowledge/ 抽取 QA → 创建/更新卡片"""
    count_created = 0
    count_skipped = 0
    count_domain = defaultdict(int)

    # 构建已有卡片索引 (source+Q → filepath)
    existing = {}
    for fpath in CARDS.rglob("*.md"):
        if fpath.name.startswith("_"):
            continue
        meta, body = parse_card(fpath)
        if meta:
            key = (meta.get("source", ""), meta.get("q", ""))
            existing[key] = fpath

    for doc_path in sorted(KNOWLEDGE.rglob("*.md")):
        rel = doc_path.relative_to(KNOWLEDGE)
        domain = rel.parts[0]  # knowledge/rag/basics.md → rag
        if domain.startswith("_"):
            continue

        qas = extract_qa_from_doc(doc_path)
        for q, a in qas:
            # 归一化 q 用于匹配
            q_norm = q.strip()
            key = (str(doc_path.relative_to(BASE)), q_norm)
            source_rel = str(doc_path.relative_to(BASE))

            if key in existing:
                if not force:
                    count_skipped += 1
                    continue
                fpath = existing[key]
            else:
                # 新建卡片
                cid = generate_card_id(domain, q_norm)
                fpath = CARDS / domain / f"{cid}.md"

            meta = {
                "id": fpath.stem,
                "domain": domain,
                "source": source_rel,
                "q": q_norm,
                "a": a,
                "created": date.today().isoformat(),
                "last_reviewed": None,
                "interval": 0,
                "ease": 2.5,
                "next_review": date.today().isoformat(),
                "reviews": 0,
            }
            body = f"**Q**: {q}\n\n**A**: {a}"
            write_card(fpath, meta, body)
            count_created += 1
            count_domain[domain] += 1

    print(f"✅ 导入完成：新建 {count_created} 张，跳过 {count_skipped} 张（已存在）")
    if count_domain:
        for d, n in sorted(count_domain.items()):
            print(f"   · {d}: +{n}")
    _update_stats()


# ── 复习模式 ──


def cmd_review(quick=False, domain=None, reset=False):
    """交互式复习"""
    cards = load_all_cards()
    today = date.today().isoformat()

    # 筛选
    if reset:
        cards_to_review = cards
    elif domain:
        cards_to_review = [(f, m, b) for f, m, b in cards if m["domain"] == domain]
    else:
        cards_to_review = [(f, m, b) for f, m, b in cards if m.get("next_review", "1970-01-01") <= today]

    if not cards_to_review:
        if reset:
            print("📭 没有卡片可重置")
        elif domain:
            print(f"📭 [{domain}] 没有到期的卡片，去学新知识吧 🎉")
        else:
            print("📭 今天没有到期的卡片，去学新知识吧 🎉")
        return

    if quick:
        cards_to_review = cards_to_review[:5]

    print(f"\n📇 本次复习：{len(cards_to_review)} 张卡片")
    if domain:
        print(f"   领域：{domain}")
    print()

    reviewed = []
    forgotten = 0
    remembered = 0
    domain_counts = defaultdict(int)

    for idx, (fpath, meta, body) in enumerate(cards_to_review, 1):
        domain_name = meta.get("domain", "?")

        print(f"─── [{idx}/{len(cards_to_review)}] {domain_name} ───")
        print(f"\n  {body}\n")
        print("  评分：0-5")

        while True:
            try:
                rating = input("  ▶ ").strip()
                if rating == "":
                    rating = "3"
                rating = int(rating)
                if 0 <= rating <= 5:
                    break
                print("  请输入 0-5 之间的数字")
            except (ValueError, EOFError):
                print("  请输入 0-5 之间的数字")

        # SM-2 更新
        meta["last_reviewed"] = today
        interval, ease, next_review = sm2_next(
            meta.get("interval", 0), meta.get("ease", 2.5), rating
        )
        meta["interval"] = interval
        meta["ease"] = ease
        meta["next_review"] = next_review
        meta["reviews"] = meta.get("reviews", 0) + 1

        write_card(fpath, meta, body)
        reviewed.append(meta)
        domain_counts[domain_name] += 1

        if rating < 3:
            forgotten += 1
            print(f"  ⚠️ 遗忘（下次间隔 {interval} 天）")
        else:
            remembered += 1
            print(f"  ✅ 记住（下次间隔 {interval} 天）")
        print()

        if reset:
            meta["interval"] = 0
            meta["ease"] = 2.5
            meta["next_review"] = date.today().isoformat()
            meta["reviews"] = 0
            write_card(fpath, meta, body)

    if reset:
        print(f"🔄 已重置所有卡片的间隔")
    else:
        total = len(cards_to_review)
        rate = remembered / total * 100 if total > 0 else 0
        domain_detail = ", ".join(f"{d}×{n}" for d, n in sorted(domain_counts.items()))
        print(f"📊 本次复习：{total} 张（{domain_detail}）")
        print(f"   记住：{remembered} | 遗忘：{forgotten} | 正确率：{rate:.0f}%")

        # 写入日志
        _log_session(total, domain_detail, forgotten, remembered, rate)
        _update_stats()


# ── 统计 ──


def _update_stats():
    """更新 stats.json"""
    cards = load_all_cards()
    today = date.today().isoformat()
    total = len(cards)
    due = sum(1 for _, m, _ in cards if m.get("next_review", "1970-01-01") <= today)

    reviewed = [m for _, m, _ in cards if m.get("last_reviewed")]
    if reviewed:
        # 最后 50 次审核的正确率
        recent = sorted(reviewed, key=lambda m: m.get("last_reviewed", ""), reverse=True)[:100]
        # 无法直接判断正确率（需要看评分），改用已复习比例
        retention = len(reviewed) / total * 100 if total > 0 else 0
    else:
        retention = 0.0

    # streak: 连续多少天有复习记录
    streak = 0
    check = date.today()
    for _ in range(365):
        day_str = check.isoformat()
        has_review = any(
            m.get("last_reviewed") == day_str for _, m, _ in cards if m.get("last_reviewed")
        )
        if has_review:
            streak += 1
            check -= timedelta(days=1)
        else:
            break

    stats = {
        "totalCards": total,
        "dueToday": due,
        "streak": streak,
        "lastReview": date.today().isoformat(),
        "retentionRate": round(retention, 1),
        "lastUpdated": date.today().isoformat(),
    }
    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def cmd_stats():
    """展示统计"""
    if not STATS_FILE.exists():
        print("📊 尚无数据")
        return
    stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))
    print(f"\n📊 复习统计")
    print(f"  卡片总数：{stats.get('totalCards', 0)}")
    print(f"  今日到期：{stats.get('dueToday', 0)}")
    print(f"  连续天数：{stats.get('streak', 0)} 🔥")
    print(f"  留存率：{stats.get('retentionRate', 0)}%")
    print(f"  上次复习：{stats.get('lastReview', '—')}")

    # 按领域统计
    cards = load_all_cards()
    by_domain = defaultdict(list)
    for fpath, meta, body in cards:
        by_domain[meta.get("domain", "?")].append(meta)
    if by_domain:
        print(f"\n  按领域：")
        for d in sorted(by_domain):
            due_d = sum(1 for m in by_domain[d] if m.get("next_review", "1970-01-01") <= date.today().isoformat())
            print(f"    {d}: {len(by_domain[d])} 张（今日到期 {due_d}）")


def _log_session(total, domain_detail, forgotten, remembered, rate):
    """写入复习日志到 _review-log.md"""
    today = date.today().isoformat()
    entry = (
        f"### {today}\n\n"
        f"- 卡片：{total}（{domain_detail}）\n"
        f"- 记住：{remembered} | 遗忘：{forgotten}\n"
        f"- 正确率：{rate:.0f}%\n\n"
    )
    # 也写一份到 memory/
    mem_file = MEMORY / f"{today}.md"
    mem_entry = (
        f"\n## 复习记录 {today}\n\n"
        f"- 复习了 {total} 张卡片（{domain_detail}）\n"
        f"- 遗忘：{forgotten} 张\n"
        f"- 正确率：{rate:.0f}%\n"
    )
    if mem_file.exists():
        mem_file.write_text(mem_file.read_text(encoding="utf-8") + mem_entry, encoding="utf-8")
    print(f"   日志已写入：memory/{today}.md")


# ── CLI ──


def main():
    parser = argparse.ArgumentParser(description="📇 复习引擎")
    parser.add_argument("command", nargs="?", default="review",
                        choices=["review", "import", "stats"],
                        help="命令：review(默认) | import | stats")
    parser.add_argument("--quick", action="store_true", help="快速复习（5 张）")
    parser.add_argument("--domain", type=str, help="指定领域，如 rag")
    parser.add_argument("--reset", action="store_true", help="重置所有间隔")
    parser.add_argument("--force", action="store_true", help="强制覆盖已有卡片")
    args = parser.parse_args()

    os.chdir(BASE)  # 工作目录切到 study-vault

    if args.command == "import":
        cmd_import(force=args.force)
    elif args.command == "stats":
        cmd_stats()
    else:
        cmd_review(quick=args.quick, domain=args.domain, reset=args.reset)


if __name__ == "__main__":
    main()
