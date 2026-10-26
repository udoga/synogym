from unittest import TestCase
from synogym.parser import DetailParser
from synogym.data_classes import Detail

class DetailParserTest(TestCase):
    def setUp(self):
        self.parser = DetailParser()

    def test_checks_detail_exists(self):
        self.assertRaises(TypeError, self.parser.parse, "")
        self.assertRaises(AssertionError, self.parser.parse, "word: happy")
        self.assertRaises(TypeError, self.parser.parse, "detail: 3")

    def test_checks_detail_fields_exist(self):
        self.assertRaises(AssertionError, self.parser.parse, "detail:\n  description: x")

    def test_checks_detail_field_values(self):
        self.assertRaises(TypeError, self.parser.parse, self.make_yaml("level", "[]"))
        self.assertRaises(TypeError, self.parser.parse, self.make_yaml("synonyms", "x"))

    def test_parse_detail(self):
        detail = self.parser.parse("""
detail:
  level: A1
  description: Feeling pleasure or satisfaction.
  synonyms: glad, cheerful
  history: From Middle English hap.
  formations: happiness, unhappy
""")
        self.assertIsInstance(detail, Detail)
        self.assertIsNone(detail.meaning_id)
        self.assertEqual("A1", detail.level)
        self.assertEqual("Feeling pleasure or satisfaction.", detail.description)
        self.assertEqual(["glad", "cheerful"], detail.synonyms)
        self.assertEqual("From Middle English hap.", detail.history)
        self.assertEqual(["happiness", "unhappy"], detail.formations)

    def make_yaml(self, field: str, value: str) -> str:
        d = {"level": "A1", "description": "x", "synonyms": "[]", "history": "x", "formations": "[]",
             field: value}
        return "detail:\n" + "".join([key + ": " + value + "\n" for key, value in d.items()])
