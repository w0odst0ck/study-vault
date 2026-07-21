# GBK

汉字编码标准，兼容 GB2312，Windows 简体中文系统默认编码。

**与 UTF-8 的区别**：UTF-8 是国际通用编码，GBK 是中文专用。
1688 等服务端用 GBK 解析 URL 中的中文字符，传中文关键词时必须显式 `quote(keyword, encoding='gbk')`。
