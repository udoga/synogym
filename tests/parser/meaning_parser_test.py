from unittest import TestCase
from synogym.parser.meaning_parser import MeaningParser

class MeaningParserTest(TestCase):
    def setUp(self):
        self.parser = MeaningParser()

    def test_checks_meanings_list_exists(self):
        self.assertRaises(TypeError, self.parser.parse, "")
        self.assertRaises(AssertionError, self.parser.parse, "word: happy")
        self.assertRaises(TypeError, self.parser.parse, "meanings: 3")

    def test_parses_empty_list(self):
        result = self.parser.parse("meanings: []")
        self.assertEqual([], result)

    def test_checks_meaning_fields_exist(self):
        self.assertRaises(TypeError, self.parser.parse, "meanings:\n- 1")
        self.assertRaises(AssertionError, self.parser.parse, "meanings:\n- pos: noun")
        self.assertRaises(AssertionError, self.parser.parse, "meanings:\n- definition: x")

    def test_checks_meaning_field_values(self):
        self.assertRaises(TypeError, self.parser.parse, "meanings:\n- pos: []\n  definition: x")
        self.assertRaises(TypeError, self.parser.parse, "meanings:\n- pos: noun\n  definition: {}")

    def test_parses_meaning(self):
        result = self.parser.parse("meanings:\n"
                                   "- definition: pleased or joyful\n"
                                   "  pos: adjective")
        self.assertEqual(1, len(result))
        self.assertEqual("", result[0].query)
        self.assertEqual("pleased or joyful", result[0].definition)
        self.assertEqual("adjective", result[0].pos)
