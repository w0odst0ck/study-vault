#!/usr/bin/env python3
"""
[ 复习引擎 ] SM-2 间隔重复 + 自动卡片提取

用法:
    python scripts/review.py                        -> 复习到期的卡片
    python scripts/review.py import                 -> 从 knowledge/ 提取卡片
    python scripts/review.py import --force         -> 覆盖已有卡片
    python scripts/review.py import --no-update-doc -> 不写回文档映射
    python scripts/review.py --count N              -> 指定复习张数
    python scripts/review.py --batch                -> 批量评分（管道输入）
    python scripts/review.py --domain rag           -> 指定领域
    python scripts/review.py --reset                -> 重置所有卡片间隔
    python scripts/review.py stats                  -> 查看统计
    python scripts/review.py stats --daily           -> 每日概况
    python scripts/review.py export                 -> 导出卡片数据到 site/data/cards.json
    python scripts/review.py deploy                  -> 导出 + 提交 + 推送到 GitHub
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
import shlex
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

# ── 路径 ──
BASE = Path(__file__).resolve().parent.parent  # study-vault/
KNOWLEDGE = BASE / "knowledge"
ANNOTATIONS = BASE / "annotations"
GLOSSARY = BASE / "glossary"
REVIEW = BASE / "review"
CARDS = REVIEW / "cards"
STATS_FILE = REVIEW / "stats.json"
LOG_FILE = REVIEW / "_review-log.md"
REFERENCES = BASE / "references"
MEMORY = BASE / "memory"

# SM-2 评分说明
RATING_HELP = """
  评分标准（SM-2）:
    0 = 完全忘记，想不起任何内容
    1 = 看到答案才想起来
    2 = 有模糊印象，但关键点错了
    3 = 勉强记起，有困难
    4 = 顺利回忆起，略有犹豫
    5 = 完美回忆，毫不费力
"""


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


# ── 文档 I/O（front matter 读写） ──


def parse_front_matter(text):
    """解析文件的 front matter，返回 (meta_dict, body_text)"""
    m = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not m:
        return None, text
    try:
        meta = json.loads(m.group(1))
    except json.JSONDecodeError:
        return None, text
    return meta, m.group(2).strip()


def write_front_matter(filepath, meta, body):
    """写回 front matter + body"""
    content = f"---\n{json.dumps(meta, ensure_ascii=False, indent=2)}\n---\n\n{body}\n"
    filepath.write_text(content, encoding="utf-8")


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


# ── 双向映射 ──


def _update_doc_card_mapping():
    """遍历知识文档，更新 front matter cards 列表 + 回顾段落卡片标记"""
    # 建立 source → [card_ids] 映射
    source_cards = defaultdict(list)
    for fpath, meta, body in load_all_cards():
        src = meta.get("source", "")
        if src:
            source_cards[src].append(meta["id"])

    for doc_path in sorted(KNOWLEDGE.rglob("*.md")):
        rel = str(doc_path.relative_to(BASE))
        if rel not in source_cards:
            continue
        card_ids = sorted(source_cards[rel])

        text = doc_path.read_text(encoding="utf-8")

        # 更新 front matter 中的 cards 字段
        meta, body = parse_front_matter(text)
        if meta is None:
            continue  # 没有 front matter，跳过

        meta["cards"] = card_ids
        meta["updated"] = date.today().isoformat()

        # 更新回顾段落的卡片标记
        # 在 ## 回顾 标题后插入 <!-- cards: xxx, yyy -->
        sections = re.split(r"^(##\s+回顾)", body, flags=re.MULTILINE)
        if len(sections) >= 3:
            # 找到回顾段落，在标题下一行插入/更新卡片注释
            review_header = sections[1]
            rest = sections[2]

            card_comment = f"<!-- cards: {', '.join(card_ids)} -->"
            # 替换/插入卡片注释行
            if rest.startswith("<!-- cards:"):
                rest = re.sub(r"^<!-- cards:.*?-->", card_comment, rest)
            else:
                rest = "\n" + card_comment + "\n" + rest.lstrip("\n")

            # 确保标题和内容之间有换行
            if not rest.startswith("\n"):
                rest = "\n" + rest
            body = sections[0] + review_header + rest

        write_front_matter(doc_path, meta, body)


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


def cmd_import(force=False, update_doc=True):
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

    # 双向映射：写回文档
    if update_doc:
        _update_doc_card_mapping()
        total_cards = len(load_all_cards())
        print(f"   📎 已回写 {total_cards} 张卡片 ID 到源文档")

    _update_stats()


# ── 导出 ──


SITE_DATA = BASE / "site" / "data"


def cmd_export():
    """导出全部数据到 site/data/（卡片 + 知识索引 + 搜索 + 术语 + 参考）"""
    SITE_DATA.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()

    # 1. 卡片
    _export_cards(SITE_DATA, today)
    # 2. 知识索引 + 搜索
    _export_knowledge(SITE_DATA, today)
    # 3. 术语表
    _export_glossary(SITE_DATA)
    # 4. 参考资源
    _export_references(SITE_DATA)
    print(f"✅ 全部数据已导出到 {SITE_DATA.relative_to(BASE)}/")


def _export_cards(site_data, today):
    cards = load_all_cards()
    export = {
        "version": 1, "exported": today,
        "totalCards": len(cards),
        "dueToday": sum(1 for _, m, _ in cards if m.get("next_review", "1970-01-01") <= today),
        "cards": [],
    }
    for fpath, meta, body in cards:
        export["cards"].append({
            "id": meta["id"], "domain": meta.get("domain", "?"),
            "q": meta["q"], "a": meta["a"],
            "interval": meta.get("interval", 0), "ease": meta.get("ease", 2.5),
            "next_review": meta.get("next_review", today),
            "last_reviewed": meta.get("last_reviewed"),
            "reviews": meta.get("reviews", 0), "created": meta.get("created", today),
        })
    (site_data / "cards.json").write_text(json.dumps(export, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📇 卡片: {len(cards)} 张")


def _export_knowledge(site_data, today):
    """知识文档目录 + 全文搜索索引"""
    index = []
    search = []
    for fpath in sorted(KNOWLEDGE.rglob("*.md")):
        if fpath.name in (".gitkeep", "_template.md"):
            continue
        rel = fpath.relative_to(KNOWLEDGE)
        text = fpath.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else fpath.stem
        domain = rel.parts[0] if len(rel.parts) > 1 else "?"

        # front matter tags
        fm, body = parse_front_matter(text)
        fm = fm or {}
        tags = fm.get("tags", [])
        created = fm.get("created", "")

        entry = {
            "id": str(rel).replace("\\", "/").replace(".md", ""),
            "title": title.strip("# "),
            "domain": domain,
            "path": str(rel).replace("\\", "/"),
            "tags": tags,
            "created": created,
        }
        index.append(entry)

        # 搜索：标题 + 正文文本（去 front matter）
        plain = re.sub(r"^---.*?^---\s*", "", text, flags=re.DOTALL | re.MULTILINE)
        plain = re.sub(r"[#*`>|\[\]()\-]+", " ", plain)
        plain = re.sub(r"\s+", " ", plain).strip()
        search.append({
            "id": entry["id"],
            "title": title.strip("# "),
            "domain": domain,
            "text": plain[:2000],  # 限制索引大小
        })

    (site_data / "knowledge-index.json").write_text(
        json.dumps({"version": 1, "exported": today, "domains": _group_by_domain(index), "docs": index},
                   ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (site_data / "search-index.json").write_text(
        json.dumps({"version": 1, "exported": today, "entries": search},
                   ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"📚 知识: {len(index)} 篇")


def _group_by_domain(entries):
    groups = {}
    for e in entries:
        d = e["domain"]
        if d not in groups:
            groups[d] = []
        groups[d].append(e["id"])
    return groups


def _export_glossary(site_data):
    """术语表"""
    items = []
    for f in sorted(GLOSSARY.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        text = f.read_text(encoding="utf-8")
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else f.stem
        desc = re.sub(r"^#.+?\n+", "", text, count=1).strip()
        # 只取第一段
        desc = desc.split("\n\n")[0].strip()
        items.append({"term": f.stem, "title": title, "desc": desc})
    (site_data / "glossary.json").write_text(
        json.dumps({"version": 1, "items": items}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"📖 术语: {len(items)} 条")


def _export_references(site_data):
    """参考资源"""
    refs = {}
    for f in sorted(REFERENCES.glob("*.md")):
        if f.name == ".gitkeep":
            continue
        category = f.stem  # books, courses, papers, repos, tools, datasets
        text = f.read_text(encoding="utf-8")
        # 拿第一行标题
        m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = m.group(1) if m else category
        # 取所有 sections
        sections = re.findall(r"^##\s+(.+)$", text, re.MULTILINE)
        refs[category] = {"title": title, "sections": sections}
    (site_data / "references.json").write_text(
        json.dumps({"version": 1, "refs": refs}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"🔗 参考: {len(refs)} 类")


def cmd_deploy():
    """导出 + 提交 + 推送，一键部署（需要 git 环境）"""
    cmd_export()
    cards_json = SITE_DATA / "cards.json"
    if not cards_json.exists():
        print("❌ site/data/cards.json 未生成")
        return 1
    ret = os.system(
        f'cd {shlex.quote(str(BASE))} && git add -f site/data/cards.json && '
        f'git commit --allow-empty -m "update: 卡片数据 $(date +%%Y-%%m-%%d)" && git push'
    )
    if ret == 0:
        print("✅ 已部署到 GitHub Pages（等待 1-2 分钟生效）")
    else:
        print("❌ 推送失败，请手动执行 git push")
    return ret


# ── 复习模式 ──


def cmd_review(count=None, batch=False, domain=None, reset=False):
    """交互式/批量复习"""
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

    if count and count > 0:
        cards_to_review = cards_to_review[:count]

    print(f"\n📇 本次复习：{len(cards_to_review)} 张卡片")
    if domain:
        print(f"   领域：{domain}")
    if batch:
        print(f"   模式：批量评分")
    print()

    reviewed = []
    forgotten = 0
    remembered = 0
    domain_counts = defaultdict(int)

    # 如果 batch 模式，预读所有评分
    batch_ratings = []
    if batch:
        import sys
        raw = sys.stdin.read().strip()
        if not raw:
            print("❌ --batch 模式需要从管道输入评分，如: echo '5 3 4' | review.py review --batch")
            return
        batch_ratings = [int(x) for x in raw.replace(",", " ").split() if x.strip().isdigit()]
        if len(batch_ratings) < len(cards_to_review):
            print(f"⚠️  评分不足（{len(batch_ratings)} < {len(cards_to_review)}），未评分卡片默认 3")
            batch_ratings.extend([3] * (len(cards_to_review) - len(batch_ratings)))
        elif len(batch_ratings) > len(cards_to_review):
            print(f"⚠️  评分过多，取前 {len(cards_to_review)} 个")
            batch_ratings = batch_ratings[:len(cards_to_review)]

    for idx, (fpath, meta, body) in enumerate(cards_to_review, 1):
        domain_name = meta.get("domain", "?")

        print(f"─── [{idx}/{len(cards_to_review)}] {domain_name} ───")
        print(f"\n  {body}\n")

        if batch:
            rating = batch_ratings[idx - 1]
            print(f"  ▶ {rating}")
        else:
            if idx == 1:
                print(RATING_HELP.strip())
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
        recent = sorted(reviewed, key=lambda m: m.get("last_reviewed", ""), reverse=True)[:100]
        retention = len(reviewed) / total * 100 if total > 0 else 0
    else:
        retention = 0.0

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

    # 按领域统计
    by_domain = defaultdict(lambda: {"total": 0, "due": 0})
    for fpath, meta, body in cards:
        d = meta.get("domain", "?")
        by_domain[d]["total"] += 1
        if meta.get("next_review", "1970-01-01") <= today:
            by_domain[d]["due"] += 1

    stats = {
        "totalCards": total,
        "dueToday": due,
        "streak": streak,
        "lastReview": date.today().isoformat(),
        "retentionRate": round(retention, 1),
        "lastUpdated": date.today().isoformat(),
        "perDomain": dict(by_domain),
    }
    STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")


def _count_docs(directory):
    """统计非模板 .md 文件"""
    return len([p for p in directory.rglob("*.md")
                if not p.name.startswith("_") and p.name != ".gitkeep"])


def cmd_stats(json_output=False, daily=False):
    """展示统计"""
    if not STATS_FILE.exists():
        print("📊 尚无数据")
        return
    stats = json.loads(STATS_FILE.read_text(encoding="utf-8"))

    if json_output:
        print(json.dumps(stats, ensure_ascii=False, indent=2))
        return

    if daily:
        total = stats.get("totalCards", 0)
        due = stats.get("dueToday", 0)
        streak = stats.get("streak", 0)
        retention = stats.get("retentionRate", 0.0)
        docs = _count_docs(KNOWLEDGE)
        anns = _count_docs(ANNOTATIONS)
        gloss = _count_docs(GLOSSARY)

        est_minutes = max(1, round(due / 2))  # 约 30 秒/张
        today = date.today().isoformat()

        print(f"\n📅 每日概况 — {today}")
        print()
        print(f"  🔥 连续复习 {streak} 天" if streak > 0 else "  🔥 开始你的第一次复习吧")
        print(f"  📇 到期 {due} 张（约 {est_minutes} 分钟）")
        print(f"  📚 卡池 {total} 张 | 知识 {docs} 篇 | 注 {anns} 篇 | 术语 {gloss} 个")
        print(f"  📈 留存率 {retention}%")

        per_domain = stats.get("perDomain", {})
        if per_domain:
            active = [(d, i) for d, i in per_domain.items() if i["due"] > 0]
            if active:
                detail = " ".join(f"{d}={i['due']}" for d, i in sorted(active))
                print(f"  🎯 待复习：{detail}")

        # 下次复习建议
        if due > 0:
            print(f"\n  💡 review.py review --count {min(due, 10)} --batch")
            print(f"     echo '5 4 3 5 5 5 4 3 5 5' | review.py review --count {min(due, 10)} --batch")
        return

    print(f"\n📊 复习统计")
    print(f"  卡片总数：{stats.get('totalCards', 0)}")
    print(f"  今日到期：{stats.get('dueToday', 0)}")
    print(f"  连续天数：{stats.get('streak', 0)} 🔥")
    print(f"  留存率：{stats.get('retentionRate', 0)}%")
    print(f"  上次复习：{stats.get('lastReview', '—')}")

    per_domain = stats.get("perDomain", {})
    if per_domain:
        print(f"\n  按领域：")
        for d in sorted(per_domain):
            info = per_domain[d]
            print(f"    {d}: {info['total']} 张（今日到期 {info['due']}）")


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
                        choices=["review", "import", "stats", "export", "deploy"],
                        help="命令：review(默认) | import | stats | export | deploy")
    parser.add_argument("--count", type=int, default=0,
                        help="复习张数，默认全部到期卡")
    parser.add_argument("--batch", action="store_true",
                        help="批量评分模式（管道输入评分，如 echo '5 3 4'）")
    parser.add_argument("--domain", type=str, help="指定领域，如 rag")
    parser.add_argument("--reset", action="store_true", help="重置所有间隔")
    parser.add_argument("--force", action="store_true", help="强制覆盖已有卡片")
    parser.add_argument("--no-update-doc", action="store_true",
                        help="不写回卡片映射到源文档（import 时）")
    parser.add_argument("--daily", action="store_true",
                        help="每日概况（stats 时）")
    parser.add_argument("--json", action="store_true",
                        help="JSON 格式输出（stats 时）")
    parser.add_argument("--quick", action="store_true",  # 保留兼容
                        help=argparse.SUPPRESS)
    args = parser.parse_args()

    os.chdir(BASE)  # 工作目录切到 study-vault

    # --quick 兼容
    count = args.count
    if args.quick and count == 0:
        count = 5

    if args.command == "import":
        cmd_import(force=args.force, update_doc=not args.no_update_doc)
    elif args.command == "stats":
        cmd_stats(json_output=args.json, daily=args.daily)
    elif args.command == "export":
        cmd_export()
    elif args.command == "deploy":
        cmd_deploy()
    else:
        cmd_review(count=count, batch=args.batch, domain=args.domain, reset=args.reset)


if __name__ == "__main__":
    main()
