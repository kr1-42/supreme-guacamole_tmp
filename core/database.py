import sqlite3
from pathlib import Path


class Database:
    """
    Wrapper minimale e sicuro per SQLite
    """

    def __init__(self, path: Path):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")

    def execute(self, query: str, params: tuple = ()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    def executescript(self, script: str):
        self.conn.executescript(script)
        self.conn.commit()

    def close(self):
        self.conn.close()
