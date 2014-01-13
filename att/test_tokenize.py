from att.test import TestCase
from att.test import MockWritableFile
from att.tokenize import word_tokenize

class TokenizeTestCase(TestCase):
  def test_word_tokenize(self):
    self.assertEqual(word_tokenize("Jestem pierogiem."), ["Jestem", "pierogiem"])
