"""See: `Dictionaries' in the documentation."""

import os
import tempfile

class Dictionary(object):
  """An abstract class to represent dictionaries."""
  def __init__(self):
    self._hunalign_cache = {}

  def EnumeratePairs(self, lang1, lang2):
    raise NotImplementedError()

  def ToEnglish(self, lang, words, try_prefixes=True):
    """Translate a word or an atomic phrase (i.e. `Scotland Yard') into
    English. If try_prefixes is set to True, all word/phrase prefixes
    will be tried if the word is not found in the dictionary to find the
    match."""
    raise NotImplementedError()

  def IsTranslation(self, lang1, words1, lang2, words2, try_prefixes=True):
    """Check, if two words (or atomic phrases, like `Scotland Yard')
    have a common translation to English. If try_prefixes is set to True,
    all word/phrase prefixes will be tried if the word is not found in the
    dictionary to find the match."""
    raise NotImplementedError()

  def CachedConvertToHunalignFormat(self, lang_a, lang_b):
    if not (lang_a, lang_b) in self._hunalign_cache or not \
        os.path.exists(self._hunalign_cache[(lang_a, lang_b)]):
      handle, filename = tempfile.mkstemp()
      output = os.fdopen(handle, 'w')
      for word_a, word_b in self.EnumeratePairs(lang_a, lang_b):
        output.write('%s @ %s\n' % (word_b, word_a))
      output.close()
      self._hunalign_cache[(lang_a, lang_b)] = filename
    return self._hunalign_cache[(lang_a, lang_b)]
