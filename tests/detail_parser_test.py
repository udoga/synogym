from unittest import TestCase
from synogym.detail_parser import DetailParser
from synogym.meaning import Meaning

class DetailParserTest(TestCase):
    def setUp(self):
        self.meaning = Meaning(query="happy", definition="pleased or joyful", pos="adjective")
        self.yaml_text = """
detail:
  level: A1
  description: Feeling pleasure or satisfaction.
  synonyms:
  - glad
  history: From Middle English hap.
  related:
  - happiness
  examples:
  - sentence: She felt happy today.
    replacements:
    - glad
    - pleased
"""

    def test_parse_detail(self):
        detail = DetailParser().parse(self.yaml_text, self.meaning)
        self.assertEqual("happy", detail.query)
        self.assertEqual("pleased or joyful", detail.definition)
        self.assertEqual("adjective", detail.pos)
        self.assertEqual("A1", detail.level)
        self.assertEqual("Feeling pleasure or satisfaction.", detail.description)
        self.assertEqual(["glad"], detail.synonyms)
        self.assertEqual("From Middle English hap.", detail.history)
        self.assertEqual(["happiness"], detail.related)
        self.assertEqual("She felt happy today.", detail.examples[0].sentence)
        self.assertEqual(["glad", "pleased"], detail.examples[0].replacements)
