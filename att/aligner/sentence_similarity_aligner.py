import math

from aligner import Aligner
from sentence_similarity_signals import SignalFactory
from att.alignment import Alignment
from att.global_context import global_context
from att.log  import VerboseLevel, LogDebugFull
from att.classifier.signal_aggregator import TuneWeights
from att.eta_clock import ETAClock
from att.utils import EnumeratePairs, Average
from att.language import Languages
from att.log import LogDebug

class SentenceSimilarityAligner(Aligner):
  def __init__(self, config):
    self._languages = [Languages.GetByCode(code)
                       for code in config['languages']]
    self._signals = []
    for signal_config in config['signals']:
      if 'runtime' in config:
        signal_config['runtime'] = config['runtime']
      self._signals.append(SignalFactory.Make(signal_config))

  def _ResetSignalCaches(self):
    for signal in self._signals:
      signal.ResetCache()

  def Train(self, training_corpus, training_set_size):
    self._TrainSignals(training_corpus, training_set_size)
    self._TuneSignalWeights(training_corpus, training_set_size)

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

  def _TrainSignals(self, training_corpus, training_set_size):
    identifiers = training_corpus.GetFirstIdentifiers(training_set_size)
    i = 0

    # some signal might want to gather some statistical information
    # about the corpus to be able to calculate anything
    for signal in self._signals:
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s",
               signal.__class__.__name__)
      signal.ProcessCorpusBeforeTraining(self._languages, training_corpus, training_set_size)
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s finished",
               signal.__class__.__name__)

    eta_clock = ETAClock(0, len(identifiers), "Training signals")
    for identifier in identifiers:
      for signal in self._signals:
        signal.ResetCache()
      reference_alignment = \
        training_corpus.GetMultilingualAlignedDocument(identifier)
      mdoc = reference_alignment.GetMultilingualDocument()
      for (lang1, sid1), (lang2, sid2), are_aligned in \
          self._EnumerateTrainingSentencePairs(mdoc, reference_alignment):
        for signal in self._signals:
          signal.AddTrainingRecord(lang1,
                                   mdoc.GetSentence(lang1, sid1),
                                   lang2,
                                   mdoc.GetSentence(lang2, sid2),
                                   are_aligned)
      eta_clock.Tick(1)
    LogDebug("[SentenceSimilarityAligner] signal states");
    for signal in self._signals:
      signal.LogStateDebug()

  def _TuneSignalWeights(self, training_corpus, training_set_size):
    LogDebug("[SentenceSimilarityAligner] signals: %s",
             ', '.join([signal.__class__.__name__ for signal in self._signals]))
    tuning_inputs = []
    for identifier in training_corpus.GetFirstIdentifiers(training_set_size):
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
                    mdoc.GetSentence(lang2, sid2)))
        tuning_inputs.append( (signals, are_aligned) )
    LogDebug("[SentenceSimilarityAligner] Tuning sentence match classifier...")
    self._weights, quality = TuneWeights(tuning_inputs)
    LogDebug("[SentenceSimilarityAligner] Sentence match classifier accuracy: %.2f%%",
             quality * 100.0)
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

  def GetMatchProbability(self, multilingual_document, lang1, sid1, lang2, sid2):
    decision = 0
    debug = []
    for signal, weight in zip(self._signals, self._weights):
      debug.append("(%s match=%.3f aggregated=%.3f weight=%.3f)" % (
          signal.__class__.__name__,
          signal.GetSimilarity(
              lang1,
              multilingual_document.GetSentence(lang1, sid1),
              lang2,
              multilingual_document.GetSentence(lang2, sid2)),
          signal.GetAggregatedMatchProbability(
              lang1,
              multilingual_document.GetSentence(lang1, sid1),
              lang2,
              multilingual_document.GetSentence(lang2, sid2)),
          weight))
      decision += signal.GetAggregatedMatchProbability(
          lang1,
          multilingual_document.GetSentence(lang1, sid1),
          lang2,
          multilingual_document.GetSentence(lang2, sid2)) * weight
    LogDebugFull('signals: %s', ', '.join(debug)) # TODO this takes time
    return decision

  def _CalculateSentenceBaselines(self, multilingual_document):
    # We want not to know the absolute classifier result, but how the
    # result can be compared to average score of a sentence.
    sentence_baselines = {}
    for lang1 in self._languages:
      for sid1 in range(multilingual_document.NumSentences(lang1)):
        random_classification_values = []
        for lang2 in self._languages:
          if lang2 == lang1:
            continue

          for sid2 in range(min(multilingual_document.NumSentences(lang2), 40)):
            random_classification_values.append(
                self.GetMatchProbability(
                    multilingual_document,
                    lang1,
                    sid1,
                    lang2,
                    sid2))
        sentence_baselines[(lang1, sid1)] = Average(random_classification_values)
    return sentence_baselines
