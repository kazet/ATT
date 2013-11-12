"""See `SentenceSimilarityAligner', `SentenceSimilarityAligner: available
signals' in the documentation."""

from att.log import LogDebug

class Signal(object):
  """An abstract class describing a signal measuring how similar two sentences
  are."""
  def __init__(self, unused_config_dict):
    self._aggregators = {}
    self._global_aggregator = self._GetAggregator()

  def AddTrainingRecord(self, lang1, sent1, lang2, sent2, are_aligned):
    """Add one training record (two sentences in two different languages
    plus an information if the sentences should be aligned or not)
    to any models the signal has."""
    if not (lang1, lang2) in self._aggregators:
      self._aggregators[(lang1, lang2)] = self._GetAggregator()
    self._aggregators[(lang1, lang2)].Aggregate(
        self.GetSimilarity(lang1, sent1, lang2, sent2),
        are_aligned)
    self._global_aggregator.Aggregate(
        self.GetSimilarity(lang1, sent1, lang2, sent2),
        are_aligned)

  def LogStateDebug(self):
    """Prints a short signal state description."""
    LogDebug("[%s] global aggregator: %s",
             self.__class__.__name__,
             str(self._global_aggregator))
    LogDebug("[%s] min bucket size=%s, for per-pair aggregators: %s",
             self.__class__.__name__,
             str(self._global_aggregator.MinBucketSize()),
             ','.join([str(k) + ': '+ str(v.MinBucketSize())
                       for k, v in self._aggregators.items()]))

  def GetAggregatedMatchProbability(self, lang1, sent1, lang2, sent2):
    """Return how big is the probability that two sentences would be aligned,
    if we would look only at the value of this signal. The trained model will
    be used to figure the probability out."""
    similarity = self.GetSimilarity(lang1, sent1, lang2, sent2)
    if not (lang1, lang2) in self._aggregators:
      return self._global_aggregator.Get(similarity)

    unused_sum, b_count = \
        self._aggregators[(lang1, lang2)].GetBucketForKey(similarity)

    if b_count > 40:  # TODO remove the const
      return self._aggregators[(lang1, lang2)].Get(similarity)
    else:
      unused_sum, b_count = \
          self._global_aggregator.GetBucketForKey(similarity)
      if b_count > 40:
        return self._global_aggregator.Get(similarity)
      else:
        return self._global_aggregator.GetGlobalAverage()

  def ProcessCorpusBeforeTraining(self,
                                  unused_languages,
                                  unused_training_corpus,
                                  unused_training_set_size):
    """Any preprocessing (i.e. word statistics) the signal may want to
    perform."""
    pass

  def GetSimilarity(self,
                    unused_lang1, unused_sent1,
                    unused_lang2, unused_sent2):
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
