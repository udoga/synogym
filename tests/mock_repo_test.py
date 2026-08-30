from unittest import TestCase
from synogym.meaning import Detail
from synogym.meaning import Meaning
from synogym.mock_repo import MockRepo

class MockRepoTest(TestCase):
    def test_creates_meaning(self):
        repo = MockRepo()
        meaning = Meaning(query="happy", definition="joyful", pos="adjective")
        repo.create_meaning(meaning)
        self.assertEqual([meaning], repo.meanings)

    def test_assigns_id_when_creates_meaning(self):
        repo = MockRepo()
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="sad", definition="unhappy", pos="adjective")]
        for meaning in meanings:
            repo.create_meaning(meaning)
        self.assertEqual([1, 2], [meaning.id for meaning in meanings])

    def test_lists_meanings_by_query(self):
        repo = MockRepo()
        happy = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        repo.create_meaning(Meaning(query="sad", definition="unhappy", pos="adjective"))
        self.assertEqual([happy], repo.list_meanings_by_query("happy"))

    def test_creates_detail_when_meaning_exists(self):
        repo = MockRepo()
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        result = repo.create_detail(detail)
        self.assertEqual(detail, result)
        self.assertEqual([detail], repo.details)

    def test_create_detail_rejects_missing_meaning(self):
        repo = MockRepo()
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(1))

    def test_create_detail_rejects_duplicate_detail(self):
        repo = MockRepo()
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        repo.create_detail(self.create_detail(meaning.id))
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(meaning.id))

    def test_reads_meaning(self):
        repo = MockRepo()
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        self.assertEqual(meaning, repo.read_meaning(meaning.id))

    def test_read_meaning_rejects_missing_meaning(self):
        repo = MockRepo()
        with self.assertRaises(ValueError):
            repo.read_meaning(1)

    def test_read_detail_returns_matching_detail(self):
        repo = MockRepo()
        meaning = repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        repo.create_detail(detail)
        self.assertEqual(detail, repo.read_detail(meaning.id))

    def test_read_detail_rejects_missing_detail(self):
        repo = MockRepo()
        with self.assertRaises(ValueError):
            repo.read_detail(1)

    def create_detail(self, detail_id: int | None) -> Detail:
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=[], history="",
                      related=[], examples=[])
