# 注：HTTP 协议基础（14-http-protocol）

> crawler-learning B1 入库后补注（2026-09-03）

## L1 术语

### ETag [ⓘ]
内容指纹（Entity Tag）：服务端按内容算出的哈希值，内容一变指纹必变。
爬虫抓取时带上 `If-None-Match: <旧 ETag>`，内容没变服务端回 304（无 body），变了回 200 + 新 body。
意义：**增量抓取**（没变就跳过解析用旧快照），省带宽省反爬暴露。
见 [glossary/ETag](../glossary/ETag.md)。

### keep-alive [ⓘ]
一个 TCP 连接上串多个 HTTP 请求（HTTP/1.1 默认长连接），省掉每次请求的三次握手。
爬虫 500 次请求不开 keep-alive = 1500 包纯握手开销。
关闭场景记忆锚：旧（HTTP/1.0 默认短）/ 说（`Connection: close`）/ 晾（空闲超时）/ 挤（连接数上限）。
见 [glossary/keep-alive](../glossary/keep-alive.md)。

### chunked [ⓘ]
分块传输编码：服务端不知道内容总长时（流式/动态生成），把 body 切成块，每块前挂 hex 长度，`0` 块收尾。
响应头 `Transfer-Encoding: chunked`（与 Content-Length 互斥）。
requests/httpx 自动解块，爬虫无感；但报文层面看得到分块。
见 [glossary/chunked](../glossary/chunked.md)。

### SameSite [ⓘ]
Cookie 的跨站携带策略（RFC 6265bis，默认 Lax）：管"什么场景带 Cookie"。
同站 ≠ 同域（同站 = scheme + 可注册域名）。Lax = 跨站顶级导航放行，跨站子资源（iframe/img/script）不放行。
爬虫意义：无头浏览器里 iframe 第三方请求不带 Cookie = 拿不到登录态，别怀疑代码。
见 [glossary/SameSite](../glossary/SameSite.md)。
