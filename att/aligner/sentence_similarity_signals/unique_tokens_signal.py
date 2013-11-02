"""See `SentenceSimilarityAligner: available signals' in the documentation."""
import re

from att.classifier import FastBucketAverage
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class UniqueTokensSignal(Signal):
  """Signal value is: max(number of special tokens (currently numbers) that
  exist in only the first sentence, num special tokens that exist only in the
  second one."""
  def __init__(self, config):
    super(UniqueTokensSignal, self).__init__(config)
    self._tokenize_dict = {}
    self._token_regexp = re.compile("^[0-9,.]+$")

  def _IsNumeric(self, word):
    """Return True if word consists only of numbers, commas and dots."""
    return self._token_regexp.match(word) is not None

  def _MemoizedWordTokenizeAndFilter(self, unused_lang, sentence):
    """Return the list of words in sentence that match self._token_regexp"""
    if not sentence in self._tokenize_dict:
      self._tokenize_dict[sentence] = \
          frozenset(filter(lambda word: self._IsNumeric(word),
                           word_tokenize(sentence)))
    return self._tokenize_dict[sentence]

  def ResetCaches(self):
    """Reset the internal per-sentence cache."""
    self._tokenize_dict = {}

  def GetSimilarity(self, lang1, sentence1, lang2, sentence2):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenizeAndFilter(lang1, sentence1)
    words2 = self._MemoizedWordTokenizeAndFilter(lang2, sentence2)
    return max(len(words1 - words2), len(words2 - words1))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 4, 4)
