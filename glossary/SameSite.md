# SameSite（Cookie 跨站策略）

Cookie 的跨站携带策略（RFC 6265bis，默认 Lax）：管"什么场景带 Cookie"。

**同站 ≠ 同域**：同站 = scheme + 可注册域名（`a.example.com` 与 `b.example.com` 同站不同域）。

**Lax**：跨站**顶级导航**（点链接进站）放行；跨站子资源（iframe/img/script）不放行。

**爬虫意义**：无头浏览器里 iframe 内的第三方请求不带 Cookie = 拿不到登录态，不是代码 bug。
