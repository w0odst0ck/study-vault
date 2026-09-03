#!/usr/bin/env python3
"""import_learning.py — study-vault 通用入库脚本（2026-09-03）

把「手册 + quiz（v2.3 题目卡片制）」的课程资料整篇迁入 study-vault（忠实迁移不重组）：
  手册 → knowledge/{domain}/{NN}-{slug}.md （frontmatter + 正文原样 + ## 回顾 节）
  quiz → 回顾节 Q/A（Q=题目原文，A=标准+记忆点）→ 调 review.py import 自动建 sm2 卡

用法：
  python3 tools/import_learning.py scan <资料目录>    # 预检不落库：手册/quiz 对、卡数、编号、去重
  python3 tools/import_learning.py apply <资料目录>   # 落库 + review.py import + _index 更新

输入约定（资料目录内 import.json，可选；缺省需 --domain）：
{
  "domain": "crawler", "source": "crawler-learning", "start_no": 14,
  "tags": ["爬虫"],
  "units": [
    {"file": "B1-http.md", "quiz": "B1-quiz.md", "slug": "http-protocol",
     "title": "HTTP 协议基础", "desc": "HTTP 报文/状态码/ETag/keep-alive/Cookie/反爬", "tags": ["HTTP"]}
  ]
}
- file：手册文件名（正文原样入文档）；quiz：同名 v2.3 卡片文件（### Tn / **题目** / **标准/记忆点**）
- slug/title/desc 必填（文档命名语义 slug）；tags 可选（缺省用顶层 tags）
- 无 import.json：需 --domain，自动扫 <资料目录>/*.md 与 *-quiz.md 配对，slug 取文件名

零第三方依赖（json/os/re/subprocess/pathlib）。
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # study-vault 根
KNOWLEDGE = BASE / "knowledge"
CARDS = BASE / "review" / "cards"
REVIEW_PY = BASE / "scripts" / "review.py"

FIELD_Q = "**题目**"
FIELD_A = "**标准/记忆点**"


# ── 基础 ──────────────────────────────────────────────

def eprint(*a):
    print(*a, file=sys.stderr)


def load_import_json(data_dir: Path) -> dict | None:
    p = data_dir / "import.json"
    if p.exists():
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return None


def domain_next_no(domain: str) -> int:
    """域内文档最大编号 + 1（跳过 _index）。"""
    d = KNOWLEDGE / domain
    if not d.exists():
        return 1
    mx = 0
    for f in d.glob("*.md"):
        if f.name == "_index.md":
            continue
        m = re.match(r"^(\d+)-", f.name)
        if m:
            mx = max(mx, int(m.group(1)))
    return mx + 1


def parse_quiz(path: Path) -> list[tuple[str, str]]:
    """解析 v2.3 quiz：按 ### 分卡，取 **题目** 与 **标准/记忆点** → [(q, a)]。"""
    text = path.read_text(encoding="utf-8")
    cards = re.split(r"^###\s+", text, flags=re.MULTILINE)[1:]
    out = []
    for card in cards:
        q = a = None
        if FIELD_Q in card:
            q = card.split(FIELD_Q, 1)[1].split("**", 1)[0].strip()
        # 标准/记忆点：字段后到下一个 **字段（作答史/状态等）前
        if FIELD_A in card:
            seg = card.split(FIELD_A, 1)[1]
            a = re.split(r"^\*\*", seg, flags=re.MULTILINE)[0].strip()
        # 去掉字段分隔符残留冒号（**题目**：xxx 的：或 :）
        if q:
            q = q.lstrip("：:").strip()
        if a:
            a = a.lstrip("：:").strip()
        if q and a:
            out.append((q, a))
        elif q or a:
            eprint(f"  ⚠️ {path.name} 某卡缺题目或标准（已跳过半卡）")
    return out


def normalize(s: str) -> str:
    """去重用归一化：空白压缩 + 去标点。"""
    return re.sub(r"[\s，。！？、；：,.!?;:()（）\"'“”‘’·-]", "", s).lower()


def existing_qs(domain: str) -> set[str]:
    d = CARDS / domain
    qs = set()
    if not d.exists():
        return qs
    for f in d.glob("*.md"):
        m = re.search(r'"q"\s*:\s*"(.*?)"\s*,', f.read_text(encoding="utf-8"))
        if m:
            qs.add(normalize(m.group(1)))
    return qs


def scan_units(data_dir: Path, cfg: dict | None) -> list[dict]:
    """展开 units：存在性 + quiz 卡数。"""
    units = []
    if cfg and cfg.get("units"):
        for u in cfg["units"]:
            fp = data_dir / u["file"]
            qp = data_dir / u.get("quiz", re.sub(r"\.md$", "-quiz.md", u["file"]))
            if not fp.exists():
                eprint(f"  ❌ 手册缺失: {u['file']}")
                sys.exit(2)
            if not qp.exists():
                eprint(f"  ❌ quiz 缺失: {qp.name}（手册 {u['file']} 需配套）")
                sys.exit(2)
            units.append({**u, "file": fp, "quiz": qp,
                          "qas": parse_quiz(qp)})
    else:
        # 自动配对：* -quiz.md 是 quiz，其余 .md 是手册
        domain = None
        for p in sorted(data_dir.glob("*.md")):
            if p.name.endswith("-quiz.md"):
                continue
            qp = data_dir / re.sub(r"\.md$", "-quiz.md", p.name)
            if not qp.exists():
                eprint(f"  ⚠️ 手册 {p.name} 无配套 quiz，跳过（需 import.json 显式声明）")
                continue
            units.append({"file": p, "quiz": qp, "slug": p.stem,
                          "title": p.stem, "desc": "", "tags": [],
                          "qas": parse_quiz(qp)})
        if not units:
            eprint("❌ 未找到 手册+quiz 配对（需 import.json 或同名 *-quiz.md）")
            sys.exit(2)
    return units


def render_doc(unit: dict, cfg: dict, no: int, total_q: int) -> str:
    """frontmatter(JSON) + 手册正文原样 + ## 回顾 Q/A。"""
    body = unit["file"].read_text(encoding="utf-8").rstrip()
    meta = {
        "status": "active",
        "created": os.environ.get("STUDY_VAULT_DATE", __import__("datetime").date.today().isoformat()),
        "updated": os.environ.get("STUDY_VAULT_DATE", __import__("datetime").date.today().isoformat()),
        "source": cfg.get("source", ""),
        "tags": unit.get("tags") or cfg.get("tags", []),
        "cards": [],
    }
    fm = json.dumps(meta, ensure_ascii=False, indent=2)
    lines = ["---", fm, "---", "", body, "", "## 回顾", ""]
    for q, a in unit["qas"]:
        qs = q.replace("\n", "\n  ")
        as_ = a.replace("\n", "\n  ")
        lines.append(f"- Q: {qs}")
        lines.append(f"  A: {as_}")
        lines.append("")
    return "\n".join(lines)


# ── 命令 ──────────────────────────────────────────────

def cmd_scan(data_dir: Path, cfg: dict | None):
    domain = cfg.get("domain") if cfg else None
    if not domain:
        eprint("❌ 缺 domain：资料目录需 import.json 或 --domain")
        sys.exit(2)
    start = cfg.get("start_no") or domain_next_no(domain)
    units = scan_units(data_dir, cfg)
    existing = existing_qs(domain)
    print(f"📥 预检：domain={domain} | 编号起点 {start} | 现有卡 {len(existing)}")
    dup_total = 0
    for i, u in enumerate(units):
        qas = u["qas"]
        dups = [q for q, _ in qas if normalize(q) in existing]
        dup_total += len(dups)
        print(f"  {start + i:02d}-{u['slug']}.md  ← {u['file'].name}（{len(qas)} 卡"
              f"{' | ⚠️去重命中 ' + str(len(dups)) + ' 条' if dups else ''}）")
        for q in dups[:3]:
            print(f"      ↳ 与现有卡重复: {q[:50]}…")
    print(f"合计 {len(units)} 文档 / {sum(len(u['qas']) for u in units)} 卡"
          f"{' / ⚠️ 去重命中 ' + str(dup_total) + ' 条' if dup_total else ' / 去重无命中 ✅'}")
    return units, start, domain


def cmd_apply(data_dir: Path, cfg: dict | None):
    units, start, domain = cmd_scan(data_dir, cfg)
    if input("确认落库？(y/N) ").strip().lower() != "y":
        print("已取消")
        return
    dom_dir = KNOWLEDGE / domain
    dom_dir.mkdir(parents=True, exist_ok=True)
    for i, u in enumerate(units):
        no = start + i
        fname = f"{no:02d}-{u['slug']}.md"
        out = dom_dir / fname
        if out.exists():
            eprint(f"  ⚠️ 已存在，跳过: {fname}")
            continue
        out.write_text(render_doc(u, cfg, no, len(u["qas"])), encoding="utf-8")
        print(f"  ✅ {fname}（{len(u['qas'])} 卡）")
    print("→ review.py import …")
    r = subprocess.run([sys.executable, str(REVIEW_PY), "import"],
                       cwd=str(BASE), capture_output=True, text=True)
    print(r.stdout[-2000:] if r.returncode == 0 else r.stderr[-2000:])
    if r.returncode != 0:
        sys.exit(1)
    print("✅ 落库完成（文档已入 knowledge/，卡已建；_index.md 需手动补行或下次维护）")


def main():
    ap = argparse.ArgumentParser(prog="import_learning",
                                 description="study-vault 通用入库：手册+quiz → knowledge 文档 + 卡")
    ap.add_argument("cmd", choices=["scan", "apply"])
    ap.add_argument("data_dir", help="资料目录（含手册 md + quiz md [+ import.json]）")
    ap.add_argument("--domain", help="域覆盖（无 import.json 时必需）")
    args = ap.parse_args()
    data_dir = Path(args.data_dir).resolve()
    if not data_dir.is_dir():
        eprint(f"❌ 目录不存在: {data_dir}")
        sys.exit(2)
    cfg = load_import_json(data_dir)
    if args.domain:
        cfg = {**(cfg or {}), "domain": args.domain}
    if args.cmd == "scan":
        cmd_scan(data_dir, cfg)
    else:
        cmd_apply(data_dir, cfg)


if __name__ == "__main__":
    main()
