"""See `SentenceSimilarityAligner: available signals' in the documentation."""

import math

from att.counter import ProbabilisticCounter
from att.classifier import FastBucketAverage
from att.utils import Flatten, EnumeratePairs
from nltk.tokenize import word_tokenize
from att.eta_clock import ETAClock
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class CooccurencySignal(Signal):
  """A signal that translates two sentences to English and scores each word
  occuring in both sentences depending on how big % of sentence pairs
  containing this word wew matches."""
  def __init__(self, config):
    super(CooccurencySignal, self).__init__(config)
    self._num_cooccurencies_in_match = ProbabilisticCounter()
    self._num_cooccurencies_outside_match = ProbabilisticCounter()

  def ProcessCorpusBeforeTraining(self,
                                  languages,
                                  training_corpus,
                                  training_set_size,
                                  dictionary):
    """Preprocess a corpus and gather cooccurency statistics."""
    identifiers = training_corpus.GetFirstIdentifiers(training_set_size)
    eta_clock = ETAClock(
        0,
        len(identifiers),
        "Preprocessing CooccurencySignal")
    for identifier in identifiers:
      self.ResetCache()
      alignment = training_corpus.GetMultilingualAlignedDocument(
          identifier)
      mdoc = alignment.GetMultilingualDocument()
      for match in alignment.GetMatches():
        for ((lang1, sid1), (lang2, sid2)) in EnumeratePairs(match):
          if lang1 not in languages or lang2 not in languages:
            continue
          first = max(0, sid2 - 2)
          last = min(mdoc.GetDocument(lang2).NumSentences(), sid2 + 3)
          for i in range(first, last):
            words1 = self._MemoizedWordTokenizeAndTranslate(
                lang1,
                mdoc.GetSentence(lang1, sid1),
                dictionary)
            words2 = self._MemoizedWordTokenizeAndTranslate(
                lang2,
                mdoc.GetSentence(lang2, i),
                dictionary)
            common = words1 & words2
            for word in common:
              if i != sid2:
                # this is not a match
                self._num_cooccurencies_outside_match.Inc(word)
              else:
                # this is a match
                self._num_cooccurencies_in_match.Inc(word)
      eta_clock.Tick()

  def _MemoizedWordTokenizeAndTranslate(self, lang, sentence, dictionary):
    """Convert a sentence to a list of word translations."""
    if not sentence in self._tokenize_dict:
      words = word_tokenize(sentence.lower())
      self._tokenize_dict[sentence] = \
          frozenset(words + Flatten([dictionary.ToEnglish(lang, word)
                             for word in words]))
    return self._tokenize_dict[sentence]

  def ResetCache(self):
    """Reset the internal per-sentence cache."""
    del self._tokenize_dict
    self._tokenize_dict = {}

  def GetSimilarity(self, lang1, sentence1, lang2, sentence2, dictionary):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenizeAndTranslate(
        lang1, sentence1, dictionary)
    words2 = self._MemoizedWordTokenizeAndTranslate(
        lang2, sentence2, dictionary)
    score = 0
    for word in words1 & words2:
      if word.__hash__() not in self._num_cooccurencies_in_match:
        continue
      score += ((1.0 * self._num_cooccurencies_in_match.Get(word)) /
        (1.0 +
         self._num_cooccurencies_in_match.Get(word) +
         self._num_cooccurencies_outside_match.GetOr0(word)))
    return score / float(math.sqrt(len(sentence1) + len(sentence2)))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0.005, 0.7, 20)
