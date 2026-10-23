from pathlib import Path
from unittest import TestCase
from synogym.data_classes import LlmCall
from synogym.db_connector import DbConnector
from synogym.repo.db.sql_llm_call_repo import SqlLlmCallRepo

class SqlLlmCallRepoTest(TestCase):
    def setUp(self):
        sql_path = str(Path(__file__).resolve().parent.parent.parent / "schema-sqlite.sql")
        config = {"type": "sqlite", "uri": ":memory:", "sql_paths": [sql_path]}
        self.connection = DbConnector().connect(config)
        self.repo = SqlLlmCallRepo(self.connection)

    def test_create_and_find(self):
        call = LlmCall(llm_name="gpt-5", reasoning_effort="minimal", operation="meanings",
                       input_token_count=10, output_token_count=20, first_token_latency=0.5,
                       generation_latency=1.2)
        saved_call = self.repo.create(call)
        self.assertEqual(saved_call, self.repo.find(saved_call.id))
