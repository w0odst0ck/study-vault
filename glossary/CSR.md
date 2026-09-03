# CSR（Client-Side Rendering）

客户端渲染：页面 JS 在浏览器端执行后渲染，源码 HTML 几乎为空壳（如 `<div id="app">`），数据靠 XHR/fetch 异步加载。

**对比 SSR**：SSR 服务端拼好 HTML（源码可解析）；CSR 源码空、需跑 JS 或抓 API。

**爬虫意义**：requests 直接抓 CSR 页 = 空壳。对策：① 无头浏览器渲染完再抓（重但通用）② 直接抓 XHR/API 接口（快但需找接口）。
