import math

from aligner import Aligner
from sentence_similarity_signals import SignalFactory
from aligner_factory import AlignerFactory
from att.alignment import Alignment
from att.global_context import global_context
from att.log  import VerboseLevel, LogDebugFull
from c_signal_aggregator import TuneWeights
from att.classifier import LinearRegression
from att.classifier import FastBucketAverage
from att.eta_clock import ETAClock
from att.utils import EnumeratePairs, Average
from att.language import Languages
from att.log import LogDebug

@AlignerFactory.Register
class SentenceSimilarityAligner(Aligner):
  def __init__(self, config):
    self._languages = [Languages.GetByCode(code)
                       for code in config['languages']]
    self._max_skip_length = config.get('max_skip_length', 5)
    self._signals = []
    for signal_config in config['signals']:
      if 'runtime' in config:
        signal_config['runtime'] = config['runtime']
      self._signals.append(SignalFactory.Make(signal_config))

  def Train(self, training_corpus):
    self._TrainSignals(training_corpus)
    self._TuneSignalWeights(training_corpus)
    self._TrainSkipLengthsPredictor(training_corpus)

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

  def _TrainSignals(self, training_corpus):
    identifiers = \
        list(training_corpus.GetMultilingualDocumentIdentifiers())
    i = 0

    # some signal might want to gather some statistical information
    # about the corpus to be able to calculate anything
    for signal in self._signals:
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s",
               signal.__class__.__name__)
      signal.ProcessCorpusBeforeTraining(self._languages, training_corpus)
      LogDebug("[SentenceSimilarityAligner] Preprocessing %s finished",
               signal.__class__.__name__)

    eta_clock = ETAClock(0, len(identifiers))
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

  def _TuneSignalWeights(self, training_corpus):
    LogDebug("[SentenceSimilarityAligner] signals: %s",
             ', '.join([signal.__class__.__name__ for signal in self._signals]))
    tuning_inputs = []
    for identifier in training_corpus.GetMultilingualDocumentIdentifiers():
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

  def _TrainSkipLengthsPredictor(self, training_corpus):
    skip_lengths = {}
    for identifier in training_corpus.GetMultilingualDocumentIdentifiers():
      last_matched_positions = {}
      reference_alignment = \
        training_corpus.GetMultilingualAlignedDocument(identifier)
      i = 0
      for match in reference_alignment.GetMatches():
        for language, sentence in match:
          if language in last_matched_positions:
            skip_length = i - last_matched_positions[language]
            if not skip_length in skip_lengths:
              skip_lengths[skip_length] = 0
            skip_lengths[skip_length] += 1
          last_matched_positions[language] = i
        i += 1  # TODO(kazet) what if there is a sentence for every language
                # that is not aligned with any other? at the same moment?
    alpha, beta = LinearRegression([(key, math.log(skip_lengths[key]))
                                    for key in skip_lengths.keys()])
    self._skip_lengths_predictor_alpha = alpha
    self._skip_lengths_predictor_beta = beta

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

  def GetSkipProbability(self, skip_length):
    return math.exp(-0.35 * skip_length)

  def Align(self, multilingual_document):
    current_positions = {}
    for language in self._languages:
      current_positions[language] = 0

    alignment = Alignment(multilingual_document)
    while True:
      best_match_quality = (0, 0)
      best_match_growset = None
      any_language_unfinished = False
      for lang in self._languages:
        any_language_unfinished = any_language_unfinished or \
            (multilingual_document.NumSentences(lang) >
             1 + current_positions[lang])
      if not any_language_unfinished:
        break
      for start_language in self._languages:
          LogDebugFull("Growing start candidate: lang=%s",
                       start_language)
          if current_positions[start_language] > \
              multilingual_document.NumSentences(start_language) - 1:
            continue
          growset = [(start_language, current_positions[start_language], 0)]
          for language in self._languages:
            if language != start_language:
              best_skip = None
              best_skip_quality = 0
              skip_available = \
                  multilingual_document.NumSentences(language) - \
                  current_positions[language]

              if skip_available == 0:
                continue

              for skip in range(0, min(self._max_skip_length, skip_available)):
                match_prob = self.GetMatchProbability(
                      multilingual_document,
                      language,
                      current_positions[language] + skip,
                      start_language,
                      current_positions[start_language])
                skip_prob = self.GetSkipProbability(skip) 
                LogDebugFull("Growing add candidate: lang=%s, sent=%d, match=%.3f skip=%.3f",
                             language,
                             current_positions[language] + skip,
                             match_prob, skip_prob)
                if match_prob * skip_prob > best_skip_quality:
                  best_skip_quality = match_prob * skip_prob
                  best_skip = skip
              growset.append( (language, current_positions[language] + best_skip, best_skip) )
              if len(growset) > 1:
                LogDebugFull("Growset candidate: %s", str(growset))
                quality = []
                for (lang1, sent1, skip1), (lang2, sent2, skip2) in EnumeratePairs(growset):
                  quality.append(
                      self.GetMatchProbability(
                          multilingual_document,
                          lang1,
                          sent1,
                          lang2,
                          sent2) *
                      self.GetSkipProbability(skip1) *
                      self.GetSkipProbability(skip2))
                if quality != []:
                  quality = (len(growset), Average(quality))
                  if best_skip is not None:
                    good = True
                    # try if it matches all languages in the growset, not only the
                    # start one
                    for grow_language, grow_sentence, grow_skip in growset:
                      assert current_positions[language] + best_skip < \
                          multilingual_document.NumSentences(language)
                      assert current_positions[grow_language] + grow_skip < \
                          multilingual_document.NumSentences(grow_language)
                      match_probability = self.GetMatchProbability(
                          multilingual_document,
                          language,
                          current_positions[language] + best_skip,
                          grow_language,
                          current_positions[grow_language] + grow_skip)
                      best_skip_probability = self.GetSkipProbability(best_skip)
                      LogDebugFull("Match add candidate lang=%s sent=%d with"
                                   " growset element lang=%s sent=%d prob=%.3f"
                                   " (classifier) * %.3f (skip penalty) [sentences: `%s' `%s']",
                                   language,
                                   current_positions[language] + best_skip,
                                   grow_language,
                                   current_positions[grow_language] + grow_skip,
                                   match_probability,
                                   best_skip_probability,
                                   multilingual_document.GetSentence(
                                       language, 
                                       current_positions[language] + best_skip).strip(),
                                   multilingual_document.GetSentence(
                                       grow_language,
                                       current_positions[grow_language] + grow_skip).strip())
                      if match_probability * best_skip_probability < 0.9:
                        good = False
                    if good:
                      LogDebugFull("Good! Match add candidate lang=%s sent=%d",
                                   language,
                                   current_positions[language] + best_skip)
                      if quality > best_match_quality:
                        best_match_quality = quality
                        best_match_growset = growset
      if not best_match_growset:
        for lang in self._languages:
          if multilingual_document.NumSentences(lang) > \
             1 + current_positions[lang]:
            current_positions[lang] += 1
        continue
      match = []
      for lang, sent, skip in best_match_growset:
        match.append( (lang, sent) )
#        for i in range(0, skip):
#          alignment.AddMatch([(lang, sent + (1 + i))])
        current_positions[lang] += skip + 1
      alignment.AddMatch(match)
    return alignment
