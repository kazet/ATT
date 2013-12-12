"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.utils import Flatten, EnumeratePairs
from att.tokenize import word_tokenize
from att.eta_clock import ETAClock
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class HapaxSignal(Signal):
  """A signal that translates two sentences to English and scores each word
  occuring in both sentences depending on how big % of sentence pairs
  containing this word wew matches."""
  def __init__(self, config):
    super(HapaxSignal, self).__init__(config)
    self._hapaxen = dict()
    self._not_hapaxen_anymore = dict()

  def ProcessCorpusBeforeTraining(self,
                                  languages,
                                  training_corpus,
                                  training_set_size,
                                  unused_dictionary):
    """Preprocess a corpus and gather cooccurency statistics."""
    identifiers = training_corpus.GetFirstIdentifiers(training_set_size)
    eta_clock = ETAClock(
        0,
        len(identifiers),
        "Preprocessing HapaxSignal")
    for identifier in identifiers:
      self.ResetCaches()
      mdoc = training_corpus.GetMultilingualDocument(identifier)
      for lang in languages:
        doc = mdoc.GetDocument(lang)
        for sent in doc.GetSentences():
          words = self._MemoizedWordTokenizeAndTranslate(lang, sent)
          for word in words:
            if word in self._hapaxen:
              del self._hapaxen[word]
              self._not_hapaxen_anymore[word] = True
            else:
              if word in self._not_hapaxen_anymore:
                continue
              else:
                self._hapaxen[word] = True

  def _MemoizedWordTokenizeAndTranslate(self, lang, sentence):
    """Convert a sentence to a list of word translations."""
    if not sentence in self._tokenize_dict:
      words = word_tokenize(sentence.lower())
      self._tokenize_dict[sentence] = frozenset(words)
    return self._tokenize_dict[sentence]

  def ResetCaches(self):
    """Reset the internal per-sentence cache."""
    self._tokenize_dict = {}

  def _GetNumHapaxen(self, words):
    num_hapaxen = 0
    for word in words:
      if word in self._hapaxen:
        num_hapaxen += 1
    return num_hapaxen

  def GetSimilarity(
      self,
      lang1, sentence1,
      lang2, sentence2,
      unused_dictionary):
    """Compute the signal value."""
    num_hapaxen1 = self._GetNumHapaxen(
        self._MemoizedWordTokenizeAndTranslate(
            lang1,
            sentence1))
    num_hapaxen2 = self._GetNumHapaxen(
        self._MemoizedWordTokenizeAndTranslate(
            lang2,
            sentence2))
    if num_hapaxen1 == 0 and num_hapaxen2 == 0:
      return 1
    elif num_hapaxen1 == 1 and num_hapaxen2 == 1:
      return 2
    elif num_hapaxen1 > 2 and num_hapaxen2 > 2:
      return 3
    else:
      return 0

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 3, 4)
