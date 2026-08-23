#!/usr/bin/env bash
# sync-cards.sh — study-vault 卡片同步全流程（幂等，手动 @ 触发）
#
# 用法: bash scripts/sync-cards.sh [--dry-run]
#   --dry-run: 只提取 + 报告，不 apply/commit/push
#
# 流程: 拉群消息 → 三层闸找"复习同步"卡片 → 去重(message_id)
#       → git 工作区检查 → apply-sync → export → commit → push → 群回执
# 设计: 幂等；失败保留现场可重跑；成功才记录 message_id + 清理；脏检查必须在 apply 前
#
# 依赖: FEISHU_APP_SECRET（~/.bashrc 或环境变量）、git、python3

set -uo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE"

DRY=0
[ "${1:-}" = "--dry-run" ] && DRY=1

PROCESSED="review/.processed-ids.json"
SYNC_FILE="review/sync-results.json"
LAST_EXTRACT="review/.last-extract.json"
NOTIFY="$HOME/.openclaw/workspace/scripts/feishu-notify.sh"
CHAT_ID="oc_0c5546a611fd44d8d0930cd5ea0bacd1"   # study-vault 同步群

# 群回执（失败不阻断主流程）
notify() {
  [ -x "$NOTIFY" ] && bash "$NOTIFY" "$1" "$CHAT_ID" chat_id 2>/dev/null || true
}

echo "📡 [1/6] 从飞书群提取复习卡片..."
export FEISHU_APP_SECRET="$(sed -n 's/^export FEISHU_APP_SECRET="\(.*\)"/\1/p' "$HOME/.bashrc" | head -1)"
if ! python3 scripts/feishu-extract.py > /tmp/sync-extract-out.json 2>/tmp/sync-extract-err.txt; then
    # 没有新卡片（extract.py exit 1 = 未找到同步数据）
    if grep -q "未找到同步数据" /tmp/sync-extract-err.txt; then
        echo "📭 没有新的复习数据"
        exit 0
    fi
    echo "❌ 提取失败:"; cat /tmp/sync-extract-err.txt
    notify "❌ study-vault 同步失败：提取异常 $(head -c 200 /tmp/sync-extract-err.txt)"
    exit 1
fi

# 去重：同一 message_id 不重复处理
MSG_ID=$(python3 -c "import json;print(json.load(open('$LAST_EXTRACT')).get('message_id',''))" 2>/dev/null || echo "")
if [ -n "$MSG_ID" ] && [ -f "$PROCESSED" ] && python3 -c "
import json,sys
try:
    ids=json.load(open('$PROCESSED'))
    sys.exit(0 if '$MSG_ID' in ids else 1)
except Exception:
    sys.exit(1)
"; then
    echo "🔄 卡片已同步过（message_id=$MSG_ID），跳过"
    exit 0
fi

CARD_COUNT=$(python3 -c "import json;print(len(json.load(open('$SYNC_FILE')).get('cards',{})))")
echo "🔄 发现 $CARD_COUNT 张新卡片"

if [ "$DRY" = "1" ]; then
    echo "🧪 dry-run：不执行 apply/commit/push"
    python3 -c "
import json
d=json.load(open('$SYNC_FILE'))
from collections import Counter
c=Counter(v['id'].split('-')[0] for v in d['cards'].values()) if all(isinstance(v,dict) and 'id' in v for v in d['cards'].values()) else Counter(k.split('-')[0] for k in d['cards'])
print('   域分布:', dict(c))" 2>/dev/null || true
    exit 0
fi

# 工作区干净检查：必须在 apply/export 之前（它们会改文件，之后检查必然脏）
# 用 git status --porcelain 含 untracked；ignored 文件（sync-results.json 等）不计数
echo "🔄 [2/7] 检查 git 工作区..."
DIRTY=$(git status --porcelain | grep -v '^!!' || true)
if [ -n "$DIRTY" ]; then
    echo "⚠️ 工作区有未提交改动，暂停同步（防止混入无关变更）："
    echo "$DIRTY" | head -10
    notify "⚠️ study-vault 同步暂停：工作区不干净，请先处理 git status"
    exit 1
fi

echo "🔄 [3/7] 合并复习记录..."
python3 scripts/apply-sync.py || { notify "❌ study-vault 同步失败：apply-sync 出错"; exit 1; }

echo "🔄 [4/7] 导出站点数据..."
python3 scripts/review.py export || { notify "❌ study-vault 同步失败：export 出错"; exit 1; }

echo "🔄 [5/7] commit + push..."
git add review/cards/ site/data/
if git diff --cached --quiet; then
    echo "📭 无实际变更（卡片状态与本地一致），跳过提交"
    rm -f "$SYNC_FILE" "$LAST_EXTRACT"
    exit 0
fi
git commit -m "sync: $CARD_COUNT 张卡片复习记录 via 飞书 [ocr: reviewed]" || exit 1
# push 带重试（网络抖动兜底）
PUSH_OK=0
for i in 1 2 3; do
    if git push origin main 2>/tmp/sync-push-err.txt; then PUSH_OK=1; break; fi
    echo "  push 失败（第 $i 次），3s 后重试..."
    sleep 3
done
if [ "$PUSH_OK" != "1" ]; then
    echo "❌ push 失败，本地 commit 已保留："; tail -3 /tmp/sync-push-err.txt
    notify "❌ study-vault 同步：push 失败（commit 已本地保留）$(tail -1 /tmp/sync-push-err.txt)"
    exit 1
fi

echo "🔄 [6/7] 记录去重 + 清理..."
python3 - "$MSG_ID" << 'EOF'
import json, sys, pathlib
BASE = pathlib.Path.cwd()
PROCESSED = BASE / "review" / ".processed-ids.json"
ids = []
if PROCESSED.exists():
    try: ids = json.loads(PROCESSED.read_text())
    except Exception: ids = []
mid = sys.argv[1]
if mid and mid not in ids:
    ids.append(mid)
PROCESSED.write_text(json.dumps(ids, ensure_ascii=False, indent=2))
EOF
rm -f "$SYNC_FILE" "$LAST_EXTRACT"

echo "✅ 同步完成：$CARD_COUNT 张卡片已入库并推送"
notify "✅ study-vault 已同步 $CARD_COUNT 张卡片（$(git log -1 --format='%h')），Pages 部署中"
