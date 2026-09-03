# keep-alive（HTTP 长连接）

一个 TCP 连接上串多个 HTTP 请求（HTTP/1.1 默认长连接），避免每次请求重新三次握手。

**关闭场景**（记忆锚：旧/说/晾/挤）：HTTP/1.0 默认短连接、`Connection: close`、空闲超时、连接数上限。

**爬虫意义**：大量请求（如 500 次）不开 keep-alive = 每次握手纯开销；requests/httpx 会话（Session）自动复用连接。
