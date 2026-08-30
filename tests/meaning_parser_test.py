from unittest import TestCase
from synogym.meaning_parser import MeaningParser

class MeaningParserTest(TestCase):
    def setUp(self):
        self.yaml_text: str = """
meanings:
- definition: pleased or joyful
  pos: adjective
"""

    def test_parse_meaning(self):
        result = MeaningParser().parse(self.yaml_text, "happy")
        meaning = result[0]
        self.assertEqual("happy", meaning.query)
        self.assertEqual("pleased or joyful", meaning.definition)
        self.assertEqual("adjective", meaning.pos)

    def test_parse_empty_meanings(self):
        result = MeaningParser().parse("meanings: []", "happy")
        self.assertEqual([], result)

    def test_parse_invalid_meaning(self):
        result = MeaningParser().parse("meanings:\n- definition: []\n", "happy")
        self.assertEqual([], result)
