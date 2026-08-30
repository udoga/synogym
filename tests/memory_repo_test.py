from unittest import TestCase
from synogym.meaning import Detail
from synogym.meaning import Meaning
from synogym.meaning import MeaningWithDetail
from synogym.memory_repo import MemoryRepo

class MemoryRepoTest(TestCase):
    def test_save_meaning_stores_meaning(self):
        repo = MemoryRepo()
        meaning = Meaning(query="happy", definition="joyful", pos="adjective")
        repo.save_meaning(meaning)
        self.assertEqual([meaning], repo.meanings)

    def test_save_meaning_assigns_list_size_as_id(self):
        repo = MemoryRepo()
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="sad", definition="unhappy", pos="adjective")]
        for meaning in meanings:
            repo.save_meaning(meaning)
        self.assertEqual([1, 2], [meaning.id for meaning in meanings])

    def test_save_meanings_saves_each_meaning(self):
        repo = MemoryRepo()
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="sad", definition="unhappy", pos="adjective")]
        result = repo.save_meanings(meanings)
        self.assertEqual(meanings, repo.meanings)
        self.assertEqual(meanings, result)
        self.assertEqual([1, 2], [meaning.id for meaning in meanings])

    def test_find_meanings_returns_matching_query(self):
        repo = MemoryRepo()
        happy = repo.save_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        repo.save_meaning(Meaning(query="sad", definition="unhappy", pos="adjective"))
        self.assertEqual([happy], repo.find_meanings("happy"))

    def test_save_detail_saves_detail_when_meaning_exists(self):
        repo = MemoryRepo()
        meaning = repo.save_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        result = repo.save_detail(detail)
        expected = MeaningWithDetail(id=meaning.id, query="happy", definition="joyful", pos="adjective", detail=detail)
        self.assertEqual(expected, result)
        self.assertEqual([detail], repo.details)

    def test_save_detail_rejects_missing_meaning(self):
        repo = MemoryRepo()
        with self.assertRaises(ValueError):
            repo.save_detail(self.create_detail(1))

    def test_save_detail_rejects_duplicate_detail(self):
        repo = MemoryRepo()
        meaning = repo.save_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        repo.save_detail(self.create_detail(meaning.id))
        with self.assertRaises(ValueError):
            repo.save_detail(self.create_detail(meaning.id))

    def test_find_meaning_with_detail_returns_matching_meaning_and_detail(self):
        repo = MemoryRepo()
        meaning = repo.save_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        expected = repo.save_detail(detail)
        self.assertEqual(expected, repo.find_meaning_with_detail(meaning.id))

    def test_find_meaning_with_detail_rejects_missing_meaning(self):
        repo = MemoryRepo()
        with self.assertRaises(ValueError):
            repo.find_meaning_with_detail(1)

    def test_find_meaning_with_detail_rejects_missing_detail(self):
        repo = MemoryRepo()
        meaning = repo.save_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        with self.assertRaises(ValueError):
            repo.find_meaning_with_detail(meaning.id)

    def create_detail(self, detail_id: int | None) -> Detail:
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=[], history="",
                      related=[], examples=[])
