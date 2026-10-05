from pathlib import Path
from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

class DbConnector:
    def connect(self, database_config: dict) -> Connection:
        engine = self._create_engine(database_config)
        connection = engine.connect()
        self._prepare_connection(connection, database_config)
        self._run_sql_files(connection, database_config.get("sql_paths", []))
        return connection

    def _create_engine(self, database_config: dict) -> Engine:
        database_type = database_config["type"]
        if database_type == "sqlite":
            return create_engine(self._create_sqlite_url(database_config), connect_args={"check_same_thread": False})
        if database_type == "postgresql":
            return create_engine(database_config["uri"])
        raise ValueError(f"Unsupported database type: {database_type}")

    def _create_sqlite_url(self, database_config: dict) -> str:
        uri = database_config["uri"]
        if uri == ":memory:":
            return "sqlite:///:memory:"
        return f"sqlite:///{uri}"

    def _prepare_connection(self, connection: Connection, database_config: dict):
        if database_config["type"] == "sqlite":
            connection.exec_driver_sql("PRAGMA foreign_keys = ON")
            connection.commit()

    def _run_sql_files(self, connection: Connection, sql_paths: list[str]):
        for sql_path in sql_paths:
            self._run_sql_file(connection, sql_path)
        connection.commit()

    def _run_sql_file(self, connection: Connection, sql_path: str):
        script = Path(sql_path).read_text()
        raw_connection = connection.connection.driver_connection
        self._run_raw_script(raw_connection, script)

    def _run_raw_script(self, raw_connection: Any, script: str):
        if hasattr(raw_connection, "executescript"):
            raw_connection.executescript(script)
        else:
            raw_connection.cursor().execute(script)
