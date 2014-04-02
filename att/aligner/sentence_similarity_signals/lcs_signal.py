"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from unidecode import unidecode

from att.classifier import FastBucketAverage
from att.utils import LongestCommonSubstring
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class LCSSignal(Signal):
  """Use the relative length of the longest common substring of both
  sentences to predict the chance that two sentences will be aligned."""
  def __init__(self, config_dict):
    super(LCSSignal, self).__init__(config_dict)
    self._max_length = config_dict.get('max_length', 50)

  def GetSimilarity(self,
                    unused_lang1, sentence1,
                    unused_lang2, sentence2,
                    unused_dictionary):
    """Compute the signal value."""
    assert(type(sentence1).__name__ in ['str', 'unicode'])
    assert(type(sentence2).__name__ in ['str', 'unicode'])
    prefix1 = unidecode(sentence1[:self._max_length]).lower()
    prefix2 = unidecode(sentence2[:self._max_length]).lower()
    return len(LongestCommonSubstring(prefix1, prefix2)) / float(len(prefix1) + len(prefix2))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0.1, 0.4, 20)
