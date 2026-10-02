import sqlite3
from pathlib import Path
from sqlite3 import Row

class SqliteConnector:
    def connect(self, database_path: str, sql_paths: list[str]) -> sqlite3.Connection:
        connection = sqlite3.connect(database_path, check_same_thread=False)
        connection.row_factory = Row
        connection.execute("PRAGMA foreign_keys = ON")
        for sql_path in sql_paths:
            connection.executescript(Path(sql_path).read_text())
        connection.commit()
        return connection
