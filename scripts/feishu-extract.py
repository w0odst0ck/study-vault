#!/usr/bin/env python3
"""
从飞书群获取最新同步消息并提取 JSON 数据
"""
import json, sys, os, pathlib, urllib.request, html

CHAT_ID = "oc_0c5546a611fd44d8d0930cd5ea0bacd1"
APP_ID = "cli_aac181b732781bb6"
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")
BASE = pathlib.Path(__file__).resolve().parent.parent


def get_token():
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["tenant_access_token"]


def get_latest_messages(token, limit=10):
    url = (
        f"https://open.feishu.cn/open-apis/im/v1/messages"
        f"?container_id_type=chat&container_id={CHAT_ID}"
        f"&page_size={limit}&sort_type=ByCreateTimeDesc"
    )
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())


def extract_json(data):
    """遍历消息列表，找 webhook 发的互动卡片，提取 JSON"""
    items = data.get("data", {}).get("items", [])
    for msg in items:
        msg_type = msg.get("msg_type")
        if msg_type != "interactive":
            continue

        try:
            body = json.loads(msg.get("body", {}).get("content", "{}"))
        except json.JSONDecodeError:
            continue

        title = body.get("title", "")
        if not title or "复习同步" not in str(title):
            continue

        # 提取 elements 中的文本内容
        full_text = ""
        elements = body.get("elements", [])
        for row in elements:
            if isinstance(row, list):
                for el in row:
                    if el.get("tag") == "text":
                        full_text += el.get("text", "")
                    elif el.get("tag") == "markdown":
                        full_text += el.get("content", "")

        # 用 html.unescape 解码 HTML 实体
        decoded = html.unescape(full_text)

        # 提取 JSON 块（在 ```json ... ``` 之间）
        start = decoded.find("```json\n")
        if start == -1:
            start = decoded.find("```\n")
        if start == -1:
            continue
        start += len("```json\n") if "```json\n" in decoded else len("```\n")
        end = decoded.rfind("```")
        if end <= start:
            continue

        json_str = decoded[start:end].strip()
        try:
            parsed = json.loads(json_str)
            if "cards" in parsed:
                return parsed, msg.get("sender", {}).get("id", "")
        except json.JSONDecodeError as e:
            print(f"JSON 解析失败: {e}", file=sys.stderr)
            continue

    return None, None


def main():
    token = get_token()
    msgs = get_latest_messages(token)
    data, sender = extract_json(msgs)

    if not data:
        print("未找到同步数据", file=sys.stderr)
        sys.exit(1)

    count = len(data.get("cards", {}))
    print(f"提取到 {count} 张卡片, 发送者: {sender}", file=sys.stderr)

    sync_file = BASE / "review" / "sync-results.json"
    sync_file.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"已写入 {sync_file}", file=sys.stderr)

    # 输出 JSON 到 stdout 供管道使用
    print(json.dumps(data))


if __name__ == "__main__":
    main()
