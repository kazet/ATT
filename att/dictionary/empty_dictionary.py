"""See: `Dictionaries' in the documentation."""

from att.dictionary.dictionary import Dictionary
from att.dictionary.dictionary_factory import DictionaryFactory

@DictionaryFactory.Register
class EmptyDictionary(object):
  """An empty dictionary."""
  def __init__(self, unused_config):
    pass

  def EnumeratePairs(self, lang1, lang2):
    return []

  def ToEnglish(self, lang, words, try_prefixes=True):
    """Translate a word or an atomic phrase (i.e. `Scotland Yard') into
    English. If try_prefixes is set to True, all word/phrase prefixes
    will be tried if the word is not found in the dictionary to find the
    match."""
    return []

  def IsTranslation(self, lang1, words1, lang2, words2):
    """Check, if two words (or atomic phrases, like `Scotland Yard')
    have a common translation to English."""
    return False

  def CachedConvertToHunalignFormat(self, lang_a, lang_b):
    return []
