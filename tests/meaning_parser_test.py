from unittest import TestCase
from synogym.meaning_parser import MeaningParser

class MeaningParserTest(TestCase):
    def setUp(self):
        self.yaml_text: str = """
meanings:
- query: happy
  definition: pleased or joyful
  part_of_speech: adjective
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

    def test_parse_full_meaning(self):
        result = MeaningParser().parse(self.yaml_text)
        meaning = result[0]
        self.assertEqual("happy", meaning.query)
        self.assertEqual("pleased or joyful", meaning.definition)
        self.assertEqual("adjective", meaning.part_of_speech)
        self.assertEqual("A1", meaning.level)
        self.assertEqual("Feeling pleasure or satisfaction.", meaning.description)
        self.assertEqual(["glad"], meaning.synonyms)
        self.assertEqual("From Middle English hap.", meaning.history)
        self.assertEqual(["happiness"], meaning.related)
        self.assertEqual(1, len(meaning.examples))
        self.assertEqual("She felt happy today.", meaning.examples[0].sentence)
        self.assertEqual(["glad", "pleased"], meaning.examples[0].replacements)

    def test_parse_empty_meanings(self):
        result = MeaningParser().parse("meanings: []")
        self.assertEqual([], result)
