from unittest import TestCase
from synogym.highlighter import Highlighter

class HighlighterTest(TestCase):
    def setUp(self):
        self.highlighter = Highlighter()

    def test_no_changes_when_does_not_have_query(self):
        text = self.highlighter.highlight("It's a sunny day.", "rainy")
        self.assertEqual("It's a sunny day.", text)

    def test_highlights_query(self):
        text = self.highlighter.highlight("It's a sunny day.", "sunny")
        self.assertEqual("It's a <em>sunny</em> day.", text)

    def test_highlights_lay_out(self):
        text = self.highlighter.highlight("The designer laid out the photos.", "lay out")
        self.assertEqual("The designer <em>laid out</em> the photos.", text)

    def test_highlights_fall_on(self):
        text = self.highlighter.highlight("My birthday falls on a Saturday", "fall on")
        self.assertEqual("My birthday <em>falls on</em> a Saturday", text)

    def test_highlights_bring_to(self):
        text = self.highlighter.highlight("Stir the soup until you bring it to a gentle boil.", "bring to")
        self.assertEqual("Stir the soup until you <em>bring</em> it <em>to</em> a gentle boil.", text)

    def test_highlights_put_to(self):
        text = self.highlighter.highlight("The news put her to tears.", "put to")
        self.assertEqual("The news <em>put</em> her <em>to</em> tears.", text)

    def test_highlights_put_to_without_middle_words(self):
        text = self.highlighter.highlight("His joke put everyone to a good mood.", "put to")
        self.assertEqual("His joke <em>put</em> everyone <em>to</em> a good mood.", text)

    def test_highlights_decimate(self):
        text = self.highlighter.highlight("The invasive beetle has decimated the region's trees.", "decimate")
        self.assertEqual("The invasive beetle has <em>decimated</em> the region's trees.", text)

    def test_highlights_tell_off(self):
        text = self.highlighter.highlight("The teacher told off the students.", "tell off")
        self.assertEqual("The teacher <em>told off</em> the students.", text)

    def test_highlights_minion(self):
        text = self.highlighter.highlight("The villain sent his minions to retrieve the stolen device.", "minion")
        self.assertEqual("The villain sent his <em>minions</em> to retrieve the stolen device.", text)

    def test_highlights_see_off(self):
        text = self.highlighter.highlight("She saw him off at the airport", "see off")
        self.assertEqual("She <em>saw</em> him <em>off</em> at the airport", text)

    def test_highlights_tut(self):
        text = self.highlighter.highlight("She tutted when he arrived late to the meeting.", "tut")
        self.assertEqual("She <em>tutted</em> when he arrived late to the meeting.", text)

    def test_highlights_shuffle(self):
        text = self.highlighter.highlight("She shuffled to the kitchen, still half asleep.", "shuffle")
        self.assertEqual("She <em>shuffled</em> to the kitchen, still half asleep.", text)

    def test_highlights_plough_on(self):
        text = self.highlighter.highlight("The team ploughed on toward their launch date.", "plough on")
        self.assertEqual("The team <em>ploughed on</em> toward their launch date.", text)
