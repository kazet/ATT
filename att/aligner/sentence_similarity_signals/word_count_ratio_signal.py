"""See `SentenceSimilarityAligner: available signals' in the documentation."""

import math

from att.classifier import FastBucketAverage
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class WordCountRatioSignal(Signal):
  """Use the ratio of word counts (log(num words in sentence 1 / num words
  in sentence 2) to predict the chance that two sentences will be aligned."""
  def __init__(self, config_dict):
    super(WordCountRatioSignal, self).__init__(config_dict)
    self._word_count_dict = {}

  def _MemoizedWordCount(self, sentence):
    """Return the number of words in the sentence. This method is cached
    because nltk.tokenize is slow."""
    if not sentence in self._word_count_dict:
      self._word_count_dict[sentence] = len(word_tokenize(sentence))
    return self._word_count_dict[sentence]

  def ResetCache(self):
    """Reset the internal per-sentence cache."""
    del self._word_count_dict
    self._word_count_dict = {}

  def GetSimilarity(self,
                    unused_lang1, sentence1,
                    unused_lang2, sentence2,
                    unused_dictionary):
    """Compute the signal value."""
    len1 = self._MemoizedWordCount(sentence1)
    len2 = self._MemoizedWordCount(sentence2)
    return math.log(float(len1) / float(len2))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(-2, 2, 100)
