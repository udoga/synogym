from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from sqlalchemy import text
from sqlalchemy.engine import Connection
from sqlalchemy.exc import OperationalError
from synogym.db_connector import DbConnector

class DbConnectorTest(TestCase):
    def test_runs_sql_files_from_config(self):
        with TemporaryDirectory() as directory:
            test_path = self._write_test_sql(directory)
            connection = self._connect(":memory:", [test_path])
            user = connection.execute(text("SELECT email FROM users")).mappings().fetchone()
            self.assertEqual("admin", user["email"])

    def test_raises_error_when_parent_directory_does_not_exist(self):
        with TemporaryDirectory() as directory:
            uri = str(Path(directory) / "data" / "app.sqlite")
            with self.assertRaises(OperationalError):
                self._connect(uri, [])

    def test_rejects_unsupported_database_type(self):
        database_config = {"type": "mysql", "uri": "mysql://localhost/synogym"}
        with self.assertRaises(ValueError):
            DbConnector().connect(database_config)

    def _connect(self, uri: str, sql_paths: list[str]) -> Connection:
        return DbConnector().connect({"type": "sqlite", "uri": uri, "sql_paths": sql_paths})

    def _write_test_sql(self, directory: str) -> str:
        sql_path = Path(directory) / "test.sql"
        sql_path.write_text("CREATE TABLE users (email TEXT); INSERT INTO users VALUES ('admin')")
        return str(sql_path)
