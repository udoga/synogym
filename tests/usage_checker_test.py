from unittest import TestCase
from synogym.usage_checker import UsageChecker

class UsageCheckerTest(TestCase):
    def setUp(self):
        self.checker = UsageChecker()

    def test_create_inflections_creates_phrasal_verb_forms(self):
        inflections = self.checker.create_inflections("tell off", "verb")
        self.assertEqual(["tell off", "telling off", "tells off", "told off"], inflections)

    def test_create_inflections_creates_three_word_phrasal_verb_forms(self):
        inflections = self.checker.create_inflections("put up with", "verb")
        self.assertEqual(["put up with", "puts up with", "putting up with"], inflections)

    def test_does_not_remove_original_query(self):
        self.assertEqual(["slower"], self.checker.create_inflections("slower", "adverb"))

    def test_create_inflections_creates_noun_plural(self):
        self.assertEqual(["experience", "experiences"], self.checker.create_inflections("experience", "noun"))

    def test_create_inflections_creates_regular_verb_forms(self):
        inflections = self.checker.create_inflections("play", "verb")
        self.assertEqual(["play", "played", "playing", "plays"], inflections)

    def test_create_inflections_creates_irregular_verb_forms(self):
        inflections = self.checker.create_inflections("think", "verb")
        self.assertEqual(["think", "thinking", "thinks", "thought"], inflections)

    def test_is_usage_example_accepts_matching_noun_usage(self):
        result = self.checker.is_usage_example("Experiences shape us.", ["experience", "experiences"], "noun")
        self.assertTrue(result)

    def test_is_usage_example_rejects_wrong_pos_usage(self):
        result = self.checker.is_usage_example("I experience joy.", ["experience", "experiences"], "noun")
        self.assertFalse(result)

    def test_is_usage_example_accepts_matching_verb_usage(self):
        self.assertTrue(self.checker.is_usage_example("I thought about life.", ["think", "thinks", "thought"], "verb"))

    def test_is_usage_example_rejects_substrings(self):
        result = self.checker.is_usage_example("A thoughtful person.", ["think", "thought"], "verb")
        self.assertFalse(result)

    def test_is_usage_example_accepts_phrases(self):
        result = self.checker.is_usage_example("The teacher told off the students.", ["told off"], "verb")
        self.assertTrue(result)
