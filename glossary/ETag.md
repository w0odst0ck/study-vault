# ETag（Entity Tag）

内容指纹：服务端按资源内容算的标识（哈希），内容一变 ETag 必变。

**用法**：请求带 `If-None-Match: <旧ETag>` → 没变回 304（无 body），变了回 200 + 新 body。

**爬虫意义**：增量抓取的核心——304 跳过解析用旧快照，省带宽、少暴露（不招 429）。
**弱验证**：服务器不给 ETag 时用 Last-Modified / If-Modified-Since 凑合。
