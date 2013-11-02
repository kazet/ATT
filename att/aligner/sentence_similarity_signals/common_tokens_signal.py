"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.utils import SetSimilarity
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class CommonTokensSignal(Signal):
  """A signal that looks for words that exist in both sentences. The signal
  value is (num words that exist in both sentences) / (num words in sentence1 +
  num words in sentence2)."""
  def __init__(self, config_dict):
    super(CommonTokensSignal, self).__init__(config_dict)
    self._tokenize_dict = {}

  def _MemoizedWordTokenize(self, sentence):
    """Cached sentence->words tokenization."""
    if not sentence in self._tokenize_dict:
      self._tokenize_dict[sentence] = frozenset(word_tokenize(sentence))
    return self._tokenize_dict[sentence]

  def ResetCaches(self):
    """Reset the internal per-sentence cache."""
    self._tokenize_dict = {}

  def GetSimilarity(self, unused_lang1, sentence1, unused_lang2, sentence2):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenize(sentence1)
    words2 = self._MemoizedWordTokenize(sentence2)
    return SetSimilarity(words1, words2)

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 0.2, 20)
