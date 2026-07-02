import uuid
import aiosqlite
from typing import List, Dict, Any

class Database:
    def __init__(self, path: str = '/data/21_elasticsearch_product_index_builder.db'):
        self.path = path
        self._conn = None

    async def init(self):
        self._conn = await aiosqlite.connect(self.path)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute('PRAGMA journal_mode=WAL')
        await self._conn.executescript('''
            CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, title TEXT NOT NULL, description TEXT, category TEXT NOT NULL, price REAL NOT NULL, created_at TEXT DEFAULT (datetime('now')));
            CREATE TABLE IF NOT EXISTS inverted_index (term TEXT NOT NULL, document_id TEXT NOT NULL, frequency INTEGER NOT NULL DEFAULT 1, PRIMARY KEY(term, document_id));
        ''')
        await self._conn.commit()

    async def close(self):
        if self._conn:
            await self._conn.close()
