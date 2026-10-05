import sqlite3
from pathlib import Path
from sqlite3 import Row

class DbConnector:
    def connect(self, database_config: dict) -> sqlite3.Connection:
        if database_config["type"] != "sqlite":
            raise ValueError(f"Unsupported database type: {database_config['type']}")
        return self._connect_sqlite(database_config)

    def _connect_sqlite(self, database_config: dict) -> sqlite3.Connection:
        uri = database_config["uri"]
        connection = sqlite3.connect(uri, uri=uri.startswith("file:"), check_same_thread=False)
        connection.row_factory = Row
        connection.execute("PRAGMA foreign_keys = ON")
        self._run_sql_files(connection, database_config.get("sql_paths", []))
        return connection

    def _run_sql_files(self, connection: sqlite3.Connection, sql_paths: list[str]):
        for sql_path in sql_paths:
            connection.executescript(Path(sql_path).read_text())
        connection.commit()
