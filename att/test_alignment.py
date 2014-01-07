from att.test import TestCase
from att.alignment import Alignment, MatchQuasiSort
from att.document import Document
from att.language import Languages
from att.multilingual_document import MultilingualDocument

class AlignmentTestCase(TestCase):
  def setUp(self):
    self.multilingual_document = MultilingualDocument([
      Document(["a", "b"], Languages.GetByCode("pl")),
      Document(["c", "d"], Languages.GetByCode("en"))])

  def test_quasi_sort(self):
    sorted_match = MatchQuasiSort([
      [('en', 5), ('pl', 4), ('de', 4)],
      [('en', 4), ('pl', 5), ('de', 5)],
      [('en', 2), ('pl', 2), ('de', 3)],
      [('en', 1), ('pl', 1), ('de', 1)],
      [('de', 6), ('pl', 5)],
      [('en', 3), ('pl', 3), ('de', 2)]])
    expected_result = [
      [('en', 1), ('pl', 1), ('de', 1)],
      [('en', 3), ('pl', 3), ('de', 2)],
      [('en', 2), ('pl', 2), ('de', 3)],
      [('en', 5), ('pl', 4), ('de', 4)],
      [('en', 4), ('pl', 5), ('de', 5)],
      [('de', 6), ('pl', 5)]]
    self.assertEqual(sorted_match, expected_result)


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
