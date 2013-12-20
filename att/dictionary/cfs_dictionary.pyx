"""See: `Dictionaries' in the documentation."""

import os

from att.log import LogDebug
from att.language import Languages
from att.utils import HaveCommonElement
from att.dictionary.dictionary import Dictionary
from att.dictionary.dictionary_factory import DictionaryFactory

@DictionaryFactory.Register
class CFSDictionary(Dictionary):
  """Dictionary subclass supporting the dictionary from
  http://cs.jhu.edu/~ccb/data/dictionaries/."""
  def __init__(self, config_dict):
    super(CFSDictionary, self).__init__()

    LogDebug("[CFSDictionary] loading...")
    per_lang_dict = {}
    config_dir = config_dict.get('runtime', {}).get('config_dir', '')
    for file_name in os.listdir(os.path.join(config_dir, config_dict['path'])):
      if len(file_name.split('.')) < 2:
        continue

      lang = file_name.split('.')[1]
      if not lang in per_lang_dict:
        per_lang_dict[lang] = []
      per_lang_dict[lang].append(file_name)

    self._to_english = {}
    # Linking word prefixes to actual words from the dictionary, so that for
    # some grammar forms, e.g. hedgehogs, all prefixes will be tried during
    # translation and a word existing in the dictionary (in this case:
    # hedgehog) will be found.
    self._english_prefix_links = {}
    self._foreign_prefix_links = {}
    self._from_english = {}
    for lang_code in config_dict['languages']:
      if lang_code == 'en':
        continue

      lang = Languages.GetByCode(lang_code)
      cfs_name = lang.GetCFSName()

      self._to_english[lang] = {}
      self._from_english[lang] = {}
      self._foreign_prefix_links[lang] = {}

      for file_name in per_lang_dict[cfs_name]:
        file_path = os.path.join(config_dir, config_dict['path'], file_name)
        file_handle = open(file_path)
        for data_line in file_handle.readlines():
          data = unicode(data_line.strip(), errors='ignore').split('\t')

          if len(data) < 2:
            continue

          english = data[0].lower().replace('_', ' ')
          foreign = data[1].lower().replace('_', ' ')

          CFSDictionary._AddPrefixLinks(self._foreign_prefix_links[lang],
                                        foreign)
          CFSDictionary._AddPrefixLinks(self._english_prefix_links, english)

          if not foreign in self._to_english[lang]:
            self._to_english[lang][foreign] = []
          self._to_english[lang][foreign].append(english)

          if not english in self._from_english[lang]:
            self._from_english[lang][english] = []
          self._from_english[lang][english].append(foreign)
    LogDebug("[CFSDictionary] loading finished")

  def EnumeratePairs(self, lang1, lang2):
    """Yields pairs, (word1, word2), where word1 and word2 both exist in the
    dictionary and have a common translation to English."""
    if lang1.IsEnglish():
      for word1, word2 in self._EnumeratePairsSingleLang(lang2):
        yield (word2, word1)
    elif lang2.IsEnglish():
      return self._EnumeratePairsSingleLang(lang1)
    else:
      for common_translation in self._from_english[lang1].iterkeys():
        if common_translation in self._from_english[lang2]:
          for word1 in self._from_english[lang1][common_translation]:
            for word2 in self._from_english[lang2][common_translation]:
              yield (word1, word2)

  def _EnumeratePairsSingleLang(self, lang):
    """Yields pairs, (word1, word2), where word1 exists in the dictionary for
    lang and word2 is its translation to English"""
    for english_word in self._from_english[lang].iterkeys():
      for foreign_word in self._from_english[lang][english_word]:
        yield (foreign_word, english_word)

  @staticmethod
  def _AddPrefixLinks(prefix_dict, word):
    """Add links from all word prefixes to the word to prefix_dict.
    If two words have common prefix, delete the link."""
    for i in range(1, len(word)):
      prefix = word[:i]
      if not prefix in prefix_dict:
        prefix_dict[prefix] = word
      elif prefix_dict[prefix] == word:
        continue
      else: # different words with same prefixes - ignore
        prefix_dict[prefix] = None

  @staticmethod
  def _GetWordWithSamePrefix(prefix_dict, word):
    """Returns the word (_AddPrefixLinks makes sure, that there is only one)
    from prefix_dict that has the longest common prefix with word."""
    for i in reversed(range(1, len(word))):
      prefix = word[:i]
      if prefix in prefix_dict and prefix_dict[prefix]:
        return prefix_dict[prefix]
    return []

  def ToEnglish(self, lang, words, try_prefixes=True):
    """Translate a word or an atomic phrase (i.e. `Scotland Yard') into
    English. If try_prefixes is set to True, all word/phrase prefixes
    will be tried if the word is not found in the dictionary to find the
    match."""
    words = words.lower()
    if lang.GetCode() == 'en':
      corrected = CFSDictionary._GetWordWithSamePrefix(
          self._english_prefix_links,
          words)
      if corrected:
        return [corrected]
      else:
        return [words]

    if not lang in self._to_english:
      return []

    if not words in self._to_english[lang]:
      corrected = CFSDictionary._GetWordWithSamePrefix(
          self._foreign_prefix_links[lang],
          words)
      if corrected:
        return self._to_english[lang][corrected]
      else:
        return []

    return self._to_english[lang][words]

  def IsTranslation(self, lang1, words1, lang2, words2):
    """Check, if two words (or atomic phrases, like `Scotland Yard')
    have a common translation to English."""
    return HaveCommonElement(self.ToEnglish(lang1, words1),
                             self.ToEnglish(lang2, words2))
