from att.test import TestCase
from att.alignment import Alignment
from att.document import Document
from att.language import Languages
from att.multilingual_document import MultilingualDocument

class AlignmentTestCase(TestCase):
  def setUp(self):
    self.multilingual_document = MultilingualDocument([
      Document(["a", "b"], Languages.GetByCode("pl")),
      Document(["c", "d"], Languages.GetByCode("en"))])

  def test_add_match(self):
    alignment = Alignment(self.multilingual_document)
    alignment.AddMatch(
      [(Languages.GetByCode("pl"), 0), (Languages.GetByCode("en"), 1)])
    alignment.AddMatch(
      [(Languages.GetByCode("pl"), 1), (Languages.GetByCode("en"), 0)])
    self.assertEqual(alignment.GetMatches(),
      [[(Languages.GetByCode("pl"), 0), (Languages.GetByCode("en"), 1)],
       [(Languages.GetByCode("pl"), 1), (Languages.GetByCode("en"), 0)]])

  def test_str(self):
    alignment = Alignment(self.multilingual_document)
    alignment.AddMatch(
      [(Languages.GetByCode("pl"), 0), (Languages.GetByCode("en"), 1)])
    alignment.AddMatch(
      [(Languages.GetByCode("pl"), 1), (Languages.GetByCode("en"), 0)])
    lines = alignment.__str__().split('\n')
    self.assertEqual(len(lines),7)
    self.assertContains(lines[0], '1')
    self.assertContains(lines[1], 'a')
    self.assertContains(lines[2], 'd')
    self.assertContains(lines[3], '2')
    self.assertContains(lines[4], 'b')
    self.assertContains(lines[5], 'c')
