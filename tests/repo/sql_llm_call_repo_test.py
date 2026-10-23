from unittest import TestCase
from synogym.data_classes import LlmCall
from synogym.db_connector import DbConnector
from synogym.repo.sqlalchemy import SqlLlmCallRepo

class SqlLlmCallRepoTest(TestCase):
    def setUp(self):
        self.connection = DbConnector().connect_test()
        self.repo = SqlLlmCallRepo(self.connection)

    def test_creates_and_finds(self):
        call = LlmCall(llm_name="gpt-5", reasoning_effort="minimal", operation="meanings",
                       input_token_count=10, output_token_count=20, first_token_latency=0.5,
                       generation_latency=1.2)
        saved_call = self.repo.create(call)
        self.assertEqual(saved_call, self.repo.find(saved_call.id))
