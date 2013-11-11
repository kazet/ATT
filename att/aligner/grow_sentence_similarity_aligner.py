import math

from sentence_similarity_aligner import SentenceSimilarityAligner
from aligner_factory import AlignerFactory
from att.alignment import Alignment
from att.log  import LogDebugFull
from att.utils import EnumeratePairs, Average

@AlignerFactory.Register
class GrowSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(GrowSentenceSimilarityAligner, self).__init__(config)
    self._max_skip_length = config.get('max_skip_length', 5)

  def GetSkipProbability(self, skip_length):
    return math.exp(-0.05 * skip_length)

  def Align(self, multilingual_document):
    self._ResetSignalCaches()

    current_positions = {}
    for language in self._languages:
      current_positions[language] = 0

    sentence_baselines = self._CalculateSentenceBaselines(multilingual_document)

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
              if best_skip is not None:
                growset.append( (language,
                                 current_positions[language] + best_skip,
                                 best_skip) )
              if len(growset) > 1:
                LogDebugFull("Growset candidate: %s", str(growset))
                quality = []
                for (lang1, sent1, skip1), (lang2, sent2, skip2) in EnumeratePairs(growset):
                  baseline = \
                    sentence_baselines[(lang1, sent1)] * \
                    sentence_baselines[(lang2, sent2)]
                  match_probability = self.GetMatchProbability(
                          multilingual_document,
                          lang1,
                          sent1,
                          lang2,
                          sent2)
                  quality.append(
                      baseline *
                      match_probability *
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
                      baseline = \
                        sentence_baselines[(language, current_positions[language] + best_skip)] * \
                        sentence_baselines[(grow_language, current_positions[grow_language] + grow_skip)]
                      if match_probability * best_skip_probability < baseline * 3.5:
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
        current_positions[lang] += skip + 1
      alignment.AddMatch(match)

    return alignment
