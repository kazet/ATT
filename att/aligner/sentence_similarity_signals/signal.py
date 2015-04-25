"""See `SentenceSimilarityAligner', `SentenceSimilarityAligner: available
signals' in the documentation."""

from att.log import LogDebug
from att.utils import Median

class Signal(object):
  """An abstract class describing a signal measuring how similar two sentences
  are."""
  def __init__(self, unused_config_dict):
    self._aggregators = {}
    self._global_aggregator = self._GetAggregator()
    self._use_per_language_aggregators = False

  def GetGlobalBuckets(self):
    for average, begin, end, unused_sum, unused_num in \
        self._global_aggregator.GetBuckets():
      yield (average, 0.5 * (begin + end))

  def SetGlobalBucketValues(self, values):
      self._global_aggregator.SetGlobalBucketValues(values)

  def AddTrainingRecord(
      self,
      lang1,
      sent1,
      lang2,
      sent2,
      are_aligned,
      dictionary):
    """Add one training record (two sentences in two different languages
    plus an information if the sentences should be aligned or not)
    to any models the signal has."""
    if self._use_per_language_aggregators:
      if not (lang1, lang2) in self._aggregators:
        self._aggregators[(lang1, lang2)] = self._GetAggregator()
      self._aggregators[(lang1, lang2)].Aggregate(
          self.GetSimilarity(lang1, sent1, lang2, sent2, dictionary),
          are_aligned)
    self._global_aggregator.Aggregate(
        self.GetSimilarity(lang1, sent1, lang2, sent2, dictionary),
        are_aligned)

  def LogStateDebug(self):
    """Prints a short signal state description."""
    LogDebug("[%s] global aggregator: %s",
             self.__class__.__name__,
             ' '.join([str(average) for average, begin, end, unused_sum, unused_num in self._global_aggregator.GetBuckets()]))
    min_bucket_size = self._global_aggregator.MinBucketSize()
    min_bucket_size_location = 'global'
    bucket_sizes = self._global_aggregator.GetBucketSizes()
    for key, value in self._aggregators.items():
      if value.MinBucketSize() < min_bucket_size:
        min_bucket_size = value.MinBucketSize()
        min_bucket_size_location = str(key)
      bucket_sizes.extend(value.GetBucketSizes())

      LogDebug("[%s] langs=%s %s",
               self.__class__.__name__,
               key,
               ' '.join([str(average) for average, begin, end, unused_sum, unused_num in value.GetBuckets()]))


    LogDebug("[%s] min bucket size=%s (%s), median bucket size=%.3f",
             self.__class__.__name__,
             min_bucket_size,
             min_bucket_size_location,
             Median(bucket_sizes))


  def GetAggregatedMatchProbability(
      self,
      lang1, sent1,
      lang2, sent2,
      dictionary):
    """Return how big is the probability that two sentences would be aligned,
    if we would look only at the value of this signal. The trained model will
    be used to figure the probability out."""
    similarity = self.GetSimilarity(lang1, sent1, lang2, sent2, dictionary)
    if self._use_per_language_aggregators:
      if not (lang1, lang2) in self._aggregators:
        return self._global_aggregator.Get(similarity)

      if self._aggregators[(lang1, lang2)].HasEnoughBuckets(similarity):
        return self._aggregators[(lang1, lang2)].Get(similarity)

    if self._global_aggregator.HasEnoughBuckets(similarity):
      return self._global_aggregator.Get(similarity)
    else:
      return self._global_aggregator.GetGlobalAverage()

  def ProcessCorpusBeforeTraining(self,
                                  unused_languages,
                                  unused_training_corpus,
                                  unused_training_set_size,
                                  unused_dictionary):
    """Any preprocessing (i.e. word statistics) the signal may want to
    perform."""
    pass

  def GetSimilarity(self,
                    unused_lang1, unused_sent1,
                    unused_lang2, unused_sent2,
                    unused_dictionary):
    """Abstract method: compute similarity between two sentences in two
    different languages."""
    raise NotImplementedError()

  def _GetAggregator(self):
    """Abstract method: return the aggregator, any already configured instance
    of FastBucketAverage, to aggregate match probabilities for different signal
    values."""
    raise NotImplementedError()

  def ResetCache(self):
    """Resets all per-sentence caches the signal may have. You may want to run
    it after each document (when there is a slight chance a cached sentence will
    be reused)."""
    pass
