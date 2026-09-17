import sqlite3
from pathlib import Path
from sqlite3 import Row

class SqliteConnector:
    def connect(self, database_path: str, schema_sql_path: str):
        connection = sqlite3.connect(database_path, check_same_thread=False)
        connection.row_factory = Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(Path(schema_sql_path).read_text())
        connection.commit()
        return connection
