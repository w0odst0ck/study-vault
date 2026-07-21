# CSS pointer-events

CSS 属性，控制元素是否响应鼠标事件。

- `pointer-events: none` → 鼠标点击/悬停穿透该元素
- `pointer-events: auto` → 正常响应

**反爬场景**：WAF 遮罩层设置 `pointer-events: none` 阻止操作页面，视觉上看到但点不了。
