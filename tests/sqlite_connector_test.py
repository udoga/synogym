from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import TestCase
from synogym.sqlite_connector import SqliteConnector

class SqliteConnectorTest(TestCase):
    def test_runs_sql_files(self):
        with TemporaryDirectory() as directory:
            test_path = self._write_test_sql(directory)
            connection = SqliteConnector().connect(":memory:", [test_path])
            user = connection.execute("SELECT email FROM users").fetchone()
            self.assertEqual("admin", user["email"])

    def _write_test_sql(self, directory: str) -> str:
        sql_path = Path(directory) / "test.sql"
        sql_path.write_text("CREATE TABLE users (email TEXT); INSERT INTO users VALUES ('admin')")
        return str(sql_path)
