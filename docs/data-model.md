# Data Model — Elasticsearch Product Index Builder

```sql
CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT, category TEXT NOT NULL, price REAL NOT NULL, created_at TEXT DEFAULT (datetime('now')));
```
