from unittest import TestCase
from synogym.formatter import Formatter

class FormatterTest(TestCase):
    def test_formatter_formats_values(self):
        formatter = Formatter("Query: {query}, POS: {pos}")
        result = formatter.format({"query": "happy", "pos": "adjective"})
        self.assertEqual("Query: happy, POS: adjective", result)
