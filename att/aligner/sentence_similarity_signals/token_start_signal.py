"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.utils import SetSimilarity
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class TokenStartSignal(Signal):
  """Use the number of common token prefixes of fixed length (determined
  in config_dict['length'] in the constructor) in both sentences to
  predict the chance that two sentences will be aligned."""
  def __init__(self, config_dict):
    super(TokenStartSignal, self).__init__(config_dict)
    self._length = config_dict.get('length', 5)
    self._tokenize_dict = {}

  def _MemoizedWordTokenize(self, sentence):
    """Return all prefixes of fixed length the sentence has. This
    function is cached because nltk.word_tokenize is slow."""
    if not sentence in self._tokenize_dict:
      tokens = []
      for token in word_tokenize(sentence):
        if len(token) < self._length:
          continue
        tokens.append(token[:self._length])
      self._tokenize_dict[sentence] = frozenset(tokens)
    return self._tokenize_dict[sentence]

  def ResetCache(self):
    """Reset the internal per-sentence cache."""
    del self._tokenize_dict
    self._tokenize_dict = {}

  def GetSimilarity(self,
                    unused_lang1, sentence1,
                    unused_lang2, sentence2,
                    unused_dictionary):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenize(sentence1)
    words2 = self._MemoizedWordTokenize(sentence2)
    return SetSimilarity(words1, words2)

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 0.2, 20)
