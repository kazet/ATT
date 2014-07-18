import math
from lxml.etree import XMLSyntaxError
from aligner import Aligner
from sentence_similarity_signals import SignalFactory
from att.alignment import Alignment
from att.classifier.signal_aggregator import TuneWeights
from att.dictionary import DictionaryFactory
from att.eta_clock import ETAClock
from sentence_similarity_signals.signals_initial_bucket_value_collection import \
  SignalsInitialBucketValueCollection
from att.global_context import global_context
from att.language import Languages
from att.log import LogDebug, VerboseLevel, LogDebugFull
from att.utils import EnumeratePairs, Average

class SentenceSimilarityAligner(Aligner):
  def __init__(self, config):
    self._languages = [Languages.GetByCode(code)
                       for code in config['languages']]

    self._signals = []
    for signal_config in config['signals']:
      if 'runtime' in config:
        signal_config['runtime'] = config['runtime']
      self._signals.append(SignalFactory.Make(signal_config))

    if not 'verification_signals' in config:
      raise Exception("No verification_signals section in the aligner config.")

    self._verification_signals = []
    for signal_config in config['verification_signals']:
      if 'runtime' in config:
        signal_config['runtime'] = config['runtime']
      self._verification_signals.append(SignalFactory.Make(signal_config))

    if self._verification_signals == []:
      raise Exception("No verification signals provided - we will not be able to" +
                      "estimate the alignment quality.")

    self._weights = [1 for unused_signal in self._signals]
    initial_bucket_value_collection = SignalsInitialBucketValueCollection()
    for signal in self._signals + self._verification_signals:
      if initial_bucket_value_collection.HasBucketValuesFor(signal.__class__.__name__):
        signal.SetGlobalBucketValues(
            initial_bucket_value_collection.GetBucketValuesFor(
                signal.__class__.__name__))

  def Verify(self, alignment, dictionary):
    match_item_set = set()
    for match in alignment.GetMatches():
      for item in match:
        if item in match_item_set:
          raise Exception("Sentence exists in more than one match - the "
                          "verification results will be fake.")
        match_item_set.add(item)

    mdoc = alignment.GetMultilingualDocument()
    qualities = []
    for signal in self._verification_signals:
      for match in alignment.GetMatches():
        values = []
        for lang1, sid1 in match:
          for lang2, sid2 in match:
            if (lang1, sid1) == (lang2, sid2):
              continue
            values.append(signal.GetAggregatedMatchProbability(
                lang1,
                mdoc.GetSentence(lang1, sid1),
                lang2,
                mdoc.GetSentence(lang2, sid2),
                dictionary))
        qualities.append(Average(values))
    return Average(qualities)

  def _ResetSignalCaches(self):
    for signal in self._signals + self._verification_signals:
      signal.ResetCache()

  def Train(self, training_corpus, training_set_size, dictionary):
    self._TrainSignals(training_corpus, training_set_size, dictionary)
    self._TuneSignalWeights(training_corpus, training_set_size, dictionary)

  def _EnumerateTrainingSentencePairs(self, mdoc, alignment):
    for match in alignment.GetMatches():
      for ((lang1, sid1), (lang2, sid2)) in EnumeratePairs(match):
        first = max(0, sid2 - 2)
        last = min(mdoc.GetDocument(lang2).NumSentences(), sid2 + 3)
        for i in range(first, last):
          if i != sid2:
            are_aligned = 0
          else:
            are_aligned = 1
          yield ((lang1, sid1), (lang2, i), are_aligned)

  def _TrainSignals(self, training_corpus, training_set_size, dictionary):
    identifiers = training_corpus.GetFirstIdentifiers(training_set_size)
    i = 0

    # some signal might want to gather some statistical information
    # about the corpus to be able to calculate anything
    for signal in self._signals + self._verification_signals:
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s",
               signal.__class__.__name__)
      signal.ProcessCorpusBeforeTraining(
          self._languages,
          training_corpus,
          training_set_size,
          dictionary)
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s finished",
               signal.__class__.__name__)

    eta_clock = ETAClock(0, len(identifiers), "Training signals")
    num_training_sentence_pairs = 0
    for identifier in identifiers:
      self._ResetSignalCaches()
      try:
        reference_alignment = \
          training_corpus.GetMultilingualAlignedDocument(identifier)
        mdoc = reference_alignment.GetMultilingualDocument()
      except XMLSyntaxError, e:
        LogDebug("[SentenceSimilarityAligner] ignoring bad document: %s",
                 identifier)
        continue

      for (lang1, sid1), (lang2, sid2), are_aligned in \
          self._EnumerateTrainingSentencePairs(mdoc, reference_alignment):
        num_training_sentence_pairs += 1
        for signal in self._signals + self._verification_signals:
          signal.AddTrainingRecord(lang1,
                                   mdoc.GetSentence(lang1, sid1),
                                   lang2,
                                   mdoc.GetSentence(lang2, sid2),
                                   are_aligned,
                                   dictionary)
      eta_clock.Tick(1)
    LogDebug("[SentenceSimilarityAligner] %d training sentence pairs" % num_training_sentence_pairs)
    bucket_debug = []
    for signal in self._signals + self._verification_signals:
      bucket_debug.append('%s %s' % (
          signal.__class__.__name__,
          ' '.join([str(val) for val, unused_pt in signal.GetGlobalBuckets()])))
    LogDebug("[SentenceSimilarityAligner] bucket debug %s" % '|'.join(bucket_debug))
    LogDebug("[SentenceSimilarityAligner] signal states")
    for signal in self._signals + self._verification_signals:
      signal.LogStateDebug()

  def _TuneSignalWeights(self, training_corpus, training_set_size, dictionary):
    LogDebug("[SentenceSimilarityAligner] signals: %s",
             ', '.join([signal.__class__.__name__ for signal in self._signals]))
    tuning_inputs = []
    identifiers = training_corpus.GetFirstIdentifiers(training_set_size)
    eta_clock = ETAClock(0, len(identifiers), "Preparing training set for tuning")
    LogDebug("[SentenceSimilarityAligner] number of training documents: %s", len(identifiers))
    for identifier in identifiers:
      reference_alignment = \
        training_corpus.GetMultilingualAlignedDocument(identifier)
      mdoc = reference_alignment.GetMultilingualDocument()
      for (lang1, sid1), (lang2, sid2), are_aligned in \
          self._EnumerateTrainingSentencePairs(mdoc, reference_alignment):
        signals = []
        for signal in self._signals:
            signals.append(
                signal.GetAggregatedMatchProbability(
                    lang1,
                    mdoc.GetSentence(lang1, sid1),
                    lang2,
                    mdoc.GetSentence(lang2, sid2),
                    dictionary))
        tuning_inputs.append( (signals, are_aligned) )
      eta_clock.Tick()
    LogDebug("[SentenceSimilarityAligner] Tuning sentence match classifier...")
    self._weights, quality = TuneWeights(tuning_inputs)
    LogDebug("[SentenceSimilarityAligner] Sentence match classifier accuracy: %.2f%%",
             quality * 100.0)
    LogDebug("[SentenceSimilarityAligner] Sentence match signal weights:\n%s",
             '\n'.join([
                '\t%s: %.3f' % (signal.__class__.__name__, weight)
                for signal, weight in zip(self._signals, self._weights)]))

    for weight in self._weights:
      if weight < 0:
        raise Exception("Negative signal weight - using it is not a good"
                        " idea. Quitting.")

    if global_context.GetArgs().verbose > VerboseLevel.DEBUG_FULL:
      for identifier in training_corpus.GetMultilingualDocumentIdentifiers():
        reference_alignment = \
          training_corpus.GetMultilingualAlignedDocument(identifier)
        mdoc = reference_alignment.GetMultilingualDocument()
        for (lang1, sid1), (lang2, sid2), are_aligned in \
            self._EnumerateTrainingSentencePairs(mdoc, reference_alignment):
          LogDebugFull("[SentenceSimilarityAligner] id1=%s, id2=%s, sentence1=`%s', sentence2=`%s'",
                   sid1,
                   sid2,
                   unicode(mdoc.GetSentence(lang1, sid1)).strip(), 
                   unicode(mdoc.GetSentence(lang2, sid2)).strip())
          decision = 0
          signals_debug = []
          for signal, weight in zip(self._signals, self._weights):
            signals_debug.append("[%s signal=%.3f aggregated=%.3f weight=%.3f]" % (
                     signal.__class__.__name__,
                     signal.GetSimilarity(
                         lang1,
                         mdoc.GetSentence(lang1, sid1),
                         lang2,
                         mdoc.GetSentence(lang2, sid2)),
                     signal.GetAggregatedMatchProbability(
                         lang1,
                         mdoc.GetSentence(lang1, sid1),
                         lang2,
                         mdoc.GetSentence(lang2, sid2)),
                     weight))
            decision += signal.GetAggregatedMatchProbability(
                lang1,
                mdoc.GetSentence(lang1, sid1),
                lang2,
                mdoc.GetSentence(lang2, sid2)) * weight
          LogDebugFull("classifier: %.3f, reality: %d, signals: %s" % (
                       decision,
                       are_aligned,
                       ', '.join(signals_debug)))
    del tuning_inputs

  def _CalculateSentenceBaselines(
        self,
        multilingual_document,
        dictionary,
        max_num_consecutive_sentences=2):
    """Returns a dictionary of (lang, sentid) -> baseline (what is the average
    classifier result for (sentence[lang, sentid], sentences[lang2, whatever])
    pairs) and (lang, sentid, num) -> baseline (what is the averae classifier
    result for (sentence[lang, sentid] + sentence[lang, sentid + 1] + ... +
    sentence[lang, sentid + num], sentences[lang2, whatever] + ... +
    sentences[lang2, whatever + num]).

    We want not to know the absolute classifier result, but how the
    result can be compared to average score of a sentence."""
    sentence_baselines = {}
    for lang1 in multilingual_document.GetLanguages():
      for sid1 in range(multilingual_document.NumSentences(lang1)):
        for num in range(1, max_num_consecutive_sentences):
          random_classification_values = []
          for lang2 in multilingual_document.GetLanguages():
            if lang2 == lang1:
              continue

            for sid2 in range(min(multilingual_document.NumSentences(lang2), 20)):
              random_classification_values.append(
                  self.GetMatchProbabilityMultipleSentences(
                      multilingual_document,
                      lang1,
                      sid1,
                      num,
                      lang2,
                      sid2,
                      num,
                      dictionary))
          sentence1 = multilingual_document.GetSentence(lang1, sid1)
          if num == 1:
            sentence_baselines[(lang1, sid1)] = Average(random_classification_values)
          sentence_baselines[(lang1, sid1, num)] = Average(random_classification_values)
          del random_classification_values
    return sentence_baselines

  def GetMatchProbability(self,
                          multilingual_document,
                          lang1,
                          sid1,
                          lang2,
                          sid2,
                          dictionary):
    decision = 0
    for signal, weight in zip(self._signals, self._weights):
      decision += signal.GetAggregatedMatchProbability(
          lang1,
          multilingual_document.GetSentence(lang1, sid1),
          lang2,
          multilingual_document.GetSentence(lang2, sid2),
          dictionary) * weight
    return decision

  def GetMatchProbabilityMultipleSentences(self,
                          multilingual_document,
                          lang1,
                          sid1,
                          num1,
                          lang2,
                          sid2,
                          num2,
                          dictionary):
    sents1 = ""
    for num in range(0, num1):
      sents1 += multilingual_document.GetSentence(lang1, sid1 + num)

    sents2 = ""
    for num in range(0, num2):
      sents2 += multilingual_document.GetSentence(lang2, sid2 + num)

    decision = 0
    for signal, weight in zip(self._signals, self._weights):
      decision += signal.GetAggregatedMatchProbability(
          lang1,
          sents1,
          lang2,
          sents2,
          dictionary) * weight
    return decision
