# chunked（分块传输编码）

服务端不知道内容总长时（流式/动态生成）的传输方式：body 切成块，每块前挂 hex 长度，`0` 块收尾。

**特征**：响应头 `Transfer-Encoding: chunked`（与 Content-Length 互斥）。

**爬虫意义**：requests/httpx 自动解块无感；报文层面看得到分块——排查"响应没 Content-Length"类问题时要认识它。
