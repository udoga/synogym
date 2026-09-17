from unittest import TestCase
from synogym.data_classes import Detail, Meaning, MeaningWithDetail
from synogym.meaning_service import MeaningService
from synogym.list_meaning_repo import ListMeaningRepo
from synogym.mock_generator import MockGenerator

class MeaningServiceTest(TestCase):
    def setUp(self):
        self.repo = ListMeaningRepo()
        self.meaning_generator = MockGenerator[str, list[Meaning]]([])
        self.detail_generator = MockGenerator[Meaning, Detail]()
        self.service = MeaningService(self.repo, self.meaning_generator, self.detail_generator)
        self.meaning = Meaning(query="happy", definition="joyful", pos="adjective")
        self.detail = Detail(meaning_id=1, level="A1", description="Feeling joy.", synonyms=[], history="",
                             formations=[], examples=[])

    def test_no_meanings_when_repo_and_generator_has_no_result(self):
        result = self.service.list_by_query("happy")
        self.assertEqual([], result)

    def test_lists_repo_meanings_when_they_exist(self):
        self.repo.create_all([self.meaning])
        result = self.service.list_by_query("happy")
        self.assertEqual([self.meaning], result)

    def test_generates_and_saves_meanings_when_repo_has_no_matches(self):
        meanings = [self.meaning, Meaning(query="happy", definition="pleased", pos="adjective")]
        self.meaning_generator.output = meanings
        result = self.service.list_by_query("happy")
        self.assertEqual(meanings, result)
        self.assertEqual(meanings, self.repo.meanings)

    def test_read_error_when_meaning_not_found(self):
        self.assertRaisesRegex(ValueError, "Meaning not found", self.service.read_meaning_with_detail, 0)

    def test_reads_meaning_with_detail_when_it_exists_in_repo(self):
        self.repo.create_all([self.meaning])
        self.repo.create_detail(self.detail)
        self.assertEqual(MeaningWithDetail(id=self.meaning.id, query="happy", definition="joyful", pos="adjective",
                                           detail=self.detail), self.service.read_meaning_with_detail(1))

    def test_saves_detail_from_generator_when_repo_only_has_meaning(self):
        self.repo.create_all([self.meaning])
        self.detail_generator.output = self.detail
        self.assertEqual(MeaningWithDetail(id=self.meaning.id, query="happy", definition="joyful", pos="adjective",
                                           detail=self.detail), self.service.read_meaning_with_detail(self.meaning.id))
        self.assertEqual([self.detail], self.repo.details)
