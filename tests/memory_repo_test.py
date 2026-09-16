from unittest import TestCase
from synogym.data_classes import Detail, Meaning, Quote
from synogym.memory_repo import MemoryRepo

class MemoryRepoTest(TestCase):
    def test_creates_meanings(self):
        repo = MemoryRepo()
        meaning = Meaning(query="happy", definition="joyful", pos="adjective")
        repo.create_meanings([meaning])
        self.assertEqual([meaning], repo.meanings)

    def test_assigns_id_when_creates_meanings(self):
        repo = MemoryRepo()
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="sad", definition="unhappy", pos="adjective")]
        repo.create_meanings(meanings)
        self.assertEqual([1, 2], [meaning.id for meaning in meanings])

    def test_lists_meanings_by_query(self):
        repo = MemoryRepo()
        happy = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        repo.create_meanings([Meaning(query="sad", definition="unhappy", pos="adjective")])
        self.assertEqual([happy], repo.list_meanings_by_query("happy"))

    def test_lists_quotes_by_query(self):
        repo = MemoryRepo()
        quote = repo.create_quotes([Quote(text="Be happy.", author="Unknown", url="https://example.com")])[0]
        repo.create_quotes([Quote(text="Be sad.", author="Unknown", url="https://example.com/sad")])
        self.assertEqual([quote], repo.list_quotes_by_query("happy"))

    def test_creates_detail_when_meaning_exists(self):
        repo = MemoryRepo()
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        result = repo.create_detail(detail)
        self.assertEqual(detail, result)
        self.assertEqual([detail], repo.details)

    def test_create_detail_rejects_missing_meaning(self):
        repo = MemoryRepo()
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(1))

    def test_create_detail_rejects_duplicate_detail(self):
        repo = MemoryRepo()
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        repo.create_detail(self.create_detail(meaning.id))
        with self.assertRaises(ValueError):
            repo.create_detail(self.create_detail(meaning.id))

    def test_reads_meaning(self):
        repo = MemoryRepo()
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        self.assertEqual(meaning, repo.read_meaning(meaning.id))

    def test_read_meaning_rejects_missing_meaning(self):
        repo = MemoryRepo()
        with self.assertRaises(ValueError):
            repo.read_meaning(1)

    def test_read_detail_returns_matching_detail(self):
        repo = MemoryRepo()
        meaning = repo.create_meanings([Meaning(query="happy", definition="joyful", pos="adjective")])[0]
        detail = self.create_detail(meaning.id)
        repo.create_detail(detail)
        self.assertEqual(detail, repo.read_detail(meaning.id))

    def test_read_detail_rejects_missing_detail(self):
        repo = MemoryRepo()
        with self.assertRaises(ValueError):
            repo.read_detail(1)

    def create_detail(self, detail_id: int | None) -> Detail:
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=[], history="",
                      formations=[], examples=[])
