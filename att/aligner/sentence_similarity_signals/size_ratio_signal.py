"""See `SentenceSimilarityAligner: available signals' in the documentation."""

import math

from att.classifier import FastBucketAverage
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class SizeRatioSignal(Signal):
  """Use the logarithm of sentence size ratio, i.e. log(num characters in
  sentence1 / num characters in sentence2) to predict the sentence
  similarity."""
  def __init__(self, config_dict):
    super(SizeRatioSignal, self).__init__(config_dict)

  def GetSimilarity(self, unused_lang1, sentence1, unused_lang2, sentence2):
    """Compute the signal value."""
    return math.log(float(len(sentence1)) / float(len(sentence2)))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(-2, 2, 100)
