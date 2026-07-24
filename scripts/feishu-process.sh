#!/usr/bin/env bash
# study-vault 飞书同步处理器
# 从飞书群获取最新的同步 JSON → 处理 → git push
#
# 用法: bash scripts/feishu-process.sh

set -euo pipefail

BASE="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BASE"

echo "📡 从飞书群提取同步数据..."
python3 scripts/feishu-extract.py

if [ ! -f review/sync-results.json ]; then
    echo "❌ 没有新的同步数据"
    exit 1
fi

CARD_COUNT=$(python3 -c "import json; d=json.load(open('review/sync-results.json')); print(len(d.get('cards',{})))")
echo "🔄 处理 $CARD_COUNT 张卡片..."

echo "  1/4 apply-sync..."
python3 scripts/apply-sync.py

echo "  2/4 review.py export..."
python3 scripts/review.py export

echo "  3/4 git commit..."
git add review/cards/ site/data/
if git diff --cached --quiet; then
    echo "📭 无变更，跳过提交"
    rm -f review/sync-results.json
    exit 0
fi
git commit -m "sync: $CARD_COUNT 张卡片 via Feishu"

echo "  4/4 git push..."
git push origin main

echo "✅ 同步完成，已推送部署"
rm -f review/sync-results.json
