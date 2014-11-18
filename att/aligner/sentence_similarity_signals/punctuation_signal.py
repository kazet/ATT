"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class PunctuationSignal(Signal):
  """The signal value is equal to num common punctuation characters in both
  sentences / (length of the first sentence + length of the second sentence)
  or 0 if both sentences are empty."""
  def __init__(self, config_dict):
    super(PunctuationSignal, self).__init__(config_dict)
    self._characters = \
        config_dict.get('characters',
                        ['.', ',', ':', ';', '(', ')', '[', ']', '?', '!'])

  def GetSimilarity(
      self,
      unused_lang1,
      sentence1,
      unused_lang2,
      sentence2,
      unused_dictionary):
    """Compute the signal value."""
    counters1 = dict([(character, 0) for character in self._characters])
    counters2 = dict([(character, 0) for character in self._characters])

    for character in sentence1:
      if character in counters1:
        counters1[character] += 1

    for character in sentence2:
      if character in counters2:
        counters2[character] += 1

    sum_common = 0
    for character in self._characters:
      sum_common += min(counters1[character], counters2[character])
    return float(sum_common) / float(len(sentence1) + len(sentence2))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 0.1, 20)
