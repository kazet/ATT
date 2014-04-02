"""See `SentenceSimilarityAligner: available signals' in the documentation."""

from att.classifier import FastBucketAverage
from att.utils import SetSimilarity
from nltk.tokenize import word_tokenize
from att.aligner.sentence_similarity_signals.signal import Signal
from att.aligner.sentence_similarity_signals.signal_factory import SignalFactory

@SignalFactory.Register
class CommonTokensSignal(Signal):
  """A signal that looks for words that exist in both sentences. The signal
  value is (num words that exist in both sentences) / (num words in sentence1 +
  num words in sentence2)."""
  def __init__(self, config_dict):
    super(CommonTokensSignal, self).__init__(config_dict)
    self._num_stopwords = config_dict.get('num_stopwords', 1000)
    self._tokenize_dict = {}
    self._word_statistics = {}

  def ProcessCorpusBeforeTraining(
      self,
      unused_languages,
      training_corpus,
      training_set_size,
      dictionary):
    """Preprocess a corpus and gather word frequency statistics."""
    for identifier in training_corpus.GetFirstIdentifiers(training_set_size):
      multilingual_document = training_corpus.GetMultilingualDocument(
          identifier)
      for language in multilingual_document.GetLanguages():
        if not language in self._word_statistics:
          self._word_statistics[language] = {}
        document = multilingual_document.GetDocument(language)
        for sentence in document.GetSentences():
          for word in word_tokenize(sentence.lower()):
            self._word_statistics[language][word] = 1 + \
                self._word_statistics[language].get(word, 0)
    self._stopwords = {}
    for language in self._word_statistics.keys():
      f = [(-frequency, word) for word, frequency in
           self._word_statistics[language].iteritems()]
      words = [word for frequency, word in sorted(f)]
      self._stopwords[language] = frozenset(words[:self._num_stopwords])

  def _MemoizedWordTokenize(self, sentence):
    """Cached sentence->words tokenization."""
    if not sentence in self._tokenize_dict:
      self._tokenize_dict[sentence] = frozenset(word_tokenize(sentence))
    return self._tokenize_dict[sentence]

  def ResetCaches(self):
    """Reset the internal per-sentence cache."""
    self._tokenize_dict = {}

  def GetSimilarity(
      self,
      lang1, sentence1,
      lang2, sentence2,
      unused_dictionary):
    """Compute the signal value."""
    words1 = self._MemoizedWordTokenize(sentence1) - self._stopwords[lang1]
    words2 = self._MemoizedWordTokenize(sentence2) - self._stopwords[lang2]
    return SetSimilarity(words1, words2)

  def _GetAggregator(self):
    """See signal.py"""
    return FastBucketAverage(0, 0.2, 20)
