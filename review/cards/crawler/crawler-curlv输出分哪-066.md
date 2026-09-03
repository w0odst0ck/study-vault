---
{
  "id": "crawler-curlv输出分哪-066",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "curl -v 输出分哪四层？为什么 HTTPS 站点看不到 HTTP/1.1 明文？",
  "a": "- 四层 = **输出层次**：① 连接建立（TCP/代理 CONNECT）② TLS 握手 ③ 发送的请求头（`>`）④ 收到的响应头（`<`）——不是报文结构！\n  - 看不到明文 = TLS 加密应用层数据 **+** HTTP/2 二进制帧（连 HTTP/1.1 文本格式都不存在）——**双保险**，不是单纯\"加密了\"",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: curl -v 输出分哪四层？为什么 HTTPS 站点看不到 HTTP/1.1 明文？

**A**: - 四层 = **输出层次**：① 连接建立（TCP/代理 CONNECT）② TLS 握手 ③ 发送的请求头（`>`）④ 收到的响应头（`<`）——不是报文结构！
  - 看不到明文 = TLS 加密应用层数据 **+** HTTP/2 二进制帧（连 HTTP/1.1 文本格式都不存在）——**双保险**，不是单纯"加密了"
