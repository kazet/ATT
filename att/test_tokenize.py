from att.test import TestCase
from att.test import MockWritableFile
from att.tokenize import tokenize

class LogTestCase(TestCase):
  def test_tokenize(self):
    self.assertEqual(tokenize("Jestem pierogiem."), ["Jestem", "pierogiem"])
