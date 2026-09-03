---
{
  "id": "crawler-chunked何时出现-065",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "chunked 何时出现？块格式长什么样？结尾标志？库怎么处理？",
  "a": "- 出现时机：**响应长度未知**（动态生成/流式输出）；长度已知的大文件反而用 Content-Length；两者互斥（RFC 9112）\n  - 块格式：`<hex长度>\\r\\n<数据>\\r\\n` 重复，**`0\\r\\n\\r\\n` 结尾**\n  - requests **默认透明解码**拼回完整 body；stream=True 才逐块",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: chunked 何时出现？块格式长什么样？结尾标志？库怎么处理？

**A**: - 出现时机：**响应长度未知**（动态生成/流式输出）；长度已知的大文件反而用 Content-Length；两者互斥（RFC 9112）
  - 块格式：`<hex长度>\r\n<数据>\r\n` 重复，**`0\r\n\r\n` 结尾**
  - requests **默认透明解码**拼回完整 body；stream=True 才逐块
