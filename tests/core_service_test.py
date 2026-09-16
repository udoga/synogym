from unittest import TestCase
from synogym.data_classes import Detail, Meaning, MeaningWithDetail, Quote
from synogym.core_service import CoreService
from synogym.memory_repo import MemoryRepo
from synogym.mock_generator import MockGenerator

class MeaningServiceTest(TestCase):
    def setUp(self):
        self.repo = MemoryRepo()
        self.meaning_generator = MockGenerator[str, list[Meaning]]([])
        self.detail_generator = MockGenerator[Meaning, Detail]()
        self.quote_fetcher = MockGenerator[str, list[Quote]]([])
        self.service = CoreService(self.repo, self.meaning_generator, self.detail_generator, self.quote_fetcher)

    def test_no_meanings_when_repo_and_generator_has_no_result(self):
        result = self.service.list_meanings("happy")
        self.assertEqual([], result)

    def test_lists_meanings_when_repo_has_it(self):
        meaning = self.repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        result = self.service.list_meanings("happy")
        self.assertEqual([meaning], result)

    def test_generates_and_saves_meanings_when_repo_has_no_matches(self):
        meanings = [Meaning(query="happy", definition="joyful", pos="adjective"),
                    Meaning(query="happy", definition="pleased", pos="adjective")]
        self.meaning_generator.output = meanings
        result = self.service.list_meanings("happy")
        self.assertEqual(meanings, result)
        self.assertEqual(meanings, self.repo.meanings)

    def test_lists_quotes_from_generator(self):
        quotes = [Quote(text="Be yourself", author="Oscar Wilde", url="https://example.com/quote")]
        self.quote_fetcher.output = quotes
        self.assertEqual(quotes, self.service.list_quotes("yourself"))

    def test_raises_error_when_repo_and_generator_has_no_detail(self):
        with self.assertRaises(ValueError):
            self.service.read_meaning_with_detail(0)

    def test_raises_error_when_repo_has_detail_but_no_meaning(self):
        self.repo.details.append(self.create_detail(1))
        with self.assertRaises(ValueError):
            self.service.read_meaning_with_detail(1)

    def test_reads_meaning_with_detail_when_it_exists_in_repo(self):
        meaning = self.repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        self.repo.create_detail(detail)
        expected = MeaningWithDetail(id=meaning.id, query="happy", definition="joyful", pos="adjective", detail=detail)
        self.assertEqual(expected, self.service.read_meaning_with_detail(meaning.id))

    def test_saves_detail_from_generator_when_repo_only_has_meaning(self):
        meaning = self.repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(meaning.id)
        self.detail_generator.output = detail
        expected = MeaningWithDetail(id=meaning.id, query="happy", definition="joyful", pos="adjective", detail=detail)
        self.assertEqual(expected, self.service.read_meaning_with_detail(meaning.id))
        self.assertEqual([detail], self.repo.details)

    def test_sets_meaning_id_on_generated_detail(self):
        meaning = self.repo.create_meaning(Meaning(query="happy", definition="joyful", pos="adjective"))
        detail = self.create_detail(None)
        self.detail_generator.output = detail
        self.service.read_meaning_with_detail(meaning.id)
        self.assertEqual(meaning.id, detail.id)

    def create_detail(self, detail_id: int | None) -> Detail:
        return Detail(id=detail_id, level="A1", description="Feeling joy.", synonyms=[], history="",
                      formations=[], examples=[])
