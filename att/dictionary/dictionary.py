"""See: `Dictionaries' in the documentation."""

class Dictionary(object):
  """An abstract class to represent dictionaries."""

  def ToEnglish(self, lang, words, try_prefixes=True):
    """Translate a word or an atomic phrase (i.e. `Scotland Yard') into
    English. If try_prefixes is set to True, all word/phrase prefixes
    will be tried if the word is not found in the dictionary to find the
    match."""
    raise NotImplementedError()

  def IsTranslation(self, lang1, words1, lang2, words2):
    """Check, if two words (or atomic phrases, like `Scotland Yard')
    have a common translation to English."""
    raise NotImplementedError()
