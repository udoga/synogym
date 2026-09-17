from unittest import TestCase
from synogym.data_classes import Detail, Meaning
from synogym.list_meaning_repo import ListMeaningRepo

class ListMeaningRepoTest(TestCase):
    def test_creates_meanings(self):
        repo = ListMeaningRepo()
        meaning = Meaning(query="happy", definition="joyful", pos="adjective")
        repo.create_all([meaning])
        self.assertEqual([meaning], repo.meanings)

    def test_assigns_id_when_creates_meanings(self):
        repo = ListMeaningRepo()
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="sad", definition="unhappy", pos="adjective")]
        repo.create_all(meanings)
        self.assertEqual([1, 2], [meaning.id for meaning in meanings])

    def test_lists_meanings_by_query(self):
        repo = ListMeaningRepo()
        happy = repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        repo.create_all([Meaning(query="sad", definition="unhappy", pos="adjective")])
        self.assertEqual([happy], repo.list_by_query("happy"))

    def test_creates_detail_when_meaning_exists(self):
        repo = ListMeaningRepo()
        meaning = repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        result = repo.create_detail(detail)
        self.assertEqual(detail, result)
        self.assertEqual([detail], repo.details)

    def test_create_detail_rejects_missing_meaning(self):
        repo = ListMeaningRepo()
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(1))

    def test_create_detail_rejects_duplicate_detail(self):
        repo = ListMeaningRepo()
        meaning = repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        repo.create_detail(self.create_detail(meaning.id))
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(meaning.id))

    def test_reads_meaning(self):
        repo = ListMeaningRepo()
        meaning = repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        self.assertEqual(meaning, repo.find(meaning.id))

    def test_find_meaning_returns_none_if_missing(self):
        repo = ListMeaningRepo()
        meaning = repo.find(1)
        self.assertIsNone(meaning)

    def test_find_detail_returns_matching_detail(self):
        repo = ListMeaningRepo()
        meaning = repo.create_all([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        repo.create_detail(detail)
        self.assertEqual(detail, repo.find_detail(meaning.id))

    def test_find_detail_returns_none_if_missing(self):
        repo = ListMeaningRepo()
        detail = repo.find_detail(1)
        self.assertIsNone(detail)

    def create_detail(self, detail_id: int | None) -> Detail:
        return Detail(meaning_id=detail_id, level="A1", description="Feeling joy.", synonyms=[], history="",
                      formations=[], examples=[])
