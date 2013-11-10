"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.utils import SetSimilarity
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class FormatSignal(Signal):
  """A signal that looks for same sentence formatting. Now it supports only
  word capitalization."""
  def __init__(self, config_dict):
    super(FormatSignal, self).__init__(config_dict)
    self._all_caps_threshold = config_dict.get('all_caps_threshold', 0.7)
    self._tokenize_dict = {}

  def IsAllCapital(self, sentence):
    """Return True if a sentence is written in ALL CAPS."""
    i = 0
    for character in sentence:
      if character.upper() == character:
        i += 1

    return i > len(sentence) * self._all_caps_threshold

  def GetSimilarity(self, unused_lang1, sentence1, unused_lang2, sentence2):
    """Compute the signal value."""
    c1 = self.IsAllCapital(sentence1)
    c2 = self.IsAllCapital(sentence2)
    if not c1 and not c2:
      return 1
    elif c1 and c2:
      return 1
    else:
      return 0

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(-0.1, 1.1, 2)
