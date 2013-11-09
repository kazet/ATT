"""See `SentenceSimilarityAligner: available signals' in the documentation."""

import math

from att.classifier import FastBucketAverage
from att.utils import Flatten
from att.dictionary import DictionaryFactory
from att.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class DictionaryWordsSignal(Signal):
  """A signal that translates two sentences and looks for common translations
  in each one."""
  def __init__(self, config):
    super(DictionaryWordsSignal, self).__init__(config)
    if 'runtime' in config:
      config['dictionary']['runtime'] = config['runtime']
    self._dictionary = DictionaryFactory.Make(config['dictionary'])
    self._tokenize_dict = {}
    self._word_statistics = {}
    self._word_prefix_links = {}

  def ProcessCorpusBeforeTraining(self, unused_languages, training_corpus):
    """Preprocess a corpus and gather English word frequency statistics."""
    for identifier in training_corpus.GetMultilingualDocumentIdentifiers():
      multilingual_document = training_corpus.GetMultilingualDocument(
          identifier)
      for language in multilingual_document.GetLanguages():
        document = multilingual_document.GetDocument(language)
        for sentence in document.GetSentences():
          for foreign_word in word_tokenize(sentence.lower()):
            for word in self._dictionary.ToEnglish(language, foreign_word):
              if not word in self._word_statistics:
                self._word_statistics[word] = 0
              self._word_statistics[word] += 1

  def _MemoizedWordTokenizeAndTranslate(self, lang, sentence):
    """Convert a sentence to a list of word translations."""
    if not sentence in self._tokenize_dict:
      words = word_tokenize(sentence.lower())
      self._tokenize_dict[sentence] = \
          frozenset(words + Flatten([self._dictionary.ToEnglish(lang, word)
                             for word in words]))
    return self._tokenize_dict[sentence]

  def ResetCaches(self):
    """Reset the internal per-sentence cache."""
    self._tokenize_dict = {}

  def GetSimilarity(self, lang1, sentence1, lang2, sentence2):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenizeAndTranslate(lang1, sentence1)
    words2 = self._MemoizedWordTokenizeAndTranslate(lang2, sentence2)
    word_score_sum = 0
    for word in words1 & words2:
      if not word in self._word_statistics:
        word_score_sum += 1.0
      else:
        word_score_sum += 1.0 / math.log(1 + self._word_statistics[word])
    return word_score_sum / float(math.sqrt(len(sentence1) + len(sentence2)))

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0.005, 0.5, 20)
