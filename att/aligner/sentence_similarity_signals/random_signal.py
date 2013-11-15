"""See `SentenceSimilarityAligner: available signals' in the documentation."""

import random

from att.classifier import FastBucketAverage
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class RandomSignal(Signal):
  """Use random noise to "predict" the chance that two sentences will be
  aligned. For testing purposes."""
  def GetSimilarity(self,
                    unused_lang1, unused_sentence1,
                    unused_lang2, unused_sentence2):
    return random.uniform(-1, 1)

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(-1, 1, 200)
