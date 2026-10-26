from unittest import TestCase
from synogym.db_connector import DbConnector
from synogym.data_classes import Detail, Example, Meaning
from synogym.repo.sqlalchemy import SqlMeaningRepo

class SqlMeaningRepoTest(TestCase):
    def setUp(self):
        self.connection = DbConnector().connect_test()
        self.repo = SqlMeaningRepo(self.connection)

    def test_meaning_operations(self):
        meaning = self.repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        self.repo.create_all([Meaning(query="sad", definition="unhappy", pos="adjective")])
        self.assertEqual([meaning], self.repo.list_by_query("happy"))
        self.assertEqual(meaning, self.repo.find(meaning.id))

    def test_detail_operations(self):
        meaning = self.repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        self.assertEqual(detail, self.repo.create_detail(detail))
        self.assertEqual(detail, self.repo.find_detail(detail.meaning_id))
        self.assertIsNone(self.repo.find_detail(123))

    def test_example_operations(self):
        meaning = self.repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        examples = [Example(sentence="She is happy.", replacements=["glad", "cheerful"])]
        self.assertEqual(examples, self.repo.create_examples(meaning.id, examples))
        self.assertEqual(examples, self.repo.list_examples(meaning.id))
        self.assertEqual([], self.repo.list_examples(123))

    def create_detail(self, meaning_id: int | None) -> Detail:
        return Detail(meaning_id=meaning_id, level="A1", description="Feeling joy.", synonyms=["glad"],
                      history="Old English.", formations=["happiness"])
