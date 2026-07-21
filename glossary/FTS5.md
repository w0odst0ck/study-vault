# FTS5（Full-Text Search 5）

SQLite 的全文搜索引擎扩展。

**特点**：内置、零配置、性能好。中文需配合 `unicode61` tokenizer 使用。
**SQL 使用**：
```sql
CREATE VIRTUAL TABLE docs_fts USING fts5(title, content, tokenize='unicode61');
SELECT * FROM docs_fts WHERE docs_fts MATCH 'keyword';
```
