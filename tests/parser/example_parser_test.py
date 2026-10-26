from unittest import TestCase
from synogym.data_classes import Example
from synogym.parser import ExampleParser

class ExampleParserTest(TestCase):
    def setUp(self):
        self.parser = ExampleParser()

    def test_checks_examples_exist(self):
        self.assertRaises(TypeError, self.parser.parse, "")
        self.assertRaises(AssertionError, self.parser.parse, "word: happy")
        self.assertRaises(TypeError, self.parser.parse, "examples: x")

    def test_checks_example_fields_exist(self):
        self.assertRaises(AssertionError, self.parser.parse, "examples:\n- sentence: x")

    def test_checks_example_field_values(self):
        self.assertRaises(TypeError, self.parser.parse, "examples:\n- sentence: []\n  replacements: []")
        self.assertRaises(ValueError, self.parser.parse, "examples:\n- sentence: x\n  replacements: x")

    def test_parse_examples(self):
        examples = self.parser.parse("""
examples:
- sentence: She felt happy today.
  replacements: glad, pleased
""")
        self.assertEqual([Example(sentence="She felt happy today.", replacements=["glad", "pleased"])], examples)
