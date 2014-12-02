from aligner_factory import AlignerFactory
from dynamic_sentence_similarity_aligner import DynamicAlign, DynamicSentenceSimilarityAligner
from sentence_similarity_aligner import SentenceSimilarityAligner

from att.alignment import Alignment
from att.find_union import FindUnion
from att.log import LogDebug
from att.max_clique import MaxClique
from att.utils import EnumeratePairs

@AlignerFactory.Register
class CombinedDynamicSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(CombinedDynamicSentenceSimilarityAligner, self).__init__(config)
    self._min_match_probability = config.get('min_match_probability', 0)
    self._config = config
    self._pivot_operand = config.get('pivot_operand', 'OR')
    self._pivot_size = config.get('pivot_size', 0)
    LogDebug("[CombinedDynamicSentenceSimilarityAligner] "
             "pivot_operand=%s pivot_size=%d min_match_probability=%.3f",
             self._pivot_operand,
             self._pivot_size,
             self._min_match_probability)

  def Align(self, multilingual_document, dictionary, ready_sentence_baselines=None):
    self._ResetSignalCaches()

    if ready_sentence_baselines:
      sentence_baselines = ready_sentence_baselines
    else:
      sentence_baselines = self._CalculateSentenceBaselines(
          multilingual_document,
          dictionary)

    languages = multilingual_document.GetLanguages()
    for language in languages:
      assert language in self._languages

    if len(languages) == 2:
      lang_a = languages[0]
      lang_b = languages[1]

      get_match_probability = \
          lambda lang_a, sent_a, lang_b, sent_b, dictionary, num_a, num_b: \
              self.GetMatchProbabilityMultipleSentences(
                  multilingual_document,
                  lang_a, sent_a, num_a,
                  lang_b, sent_b, num_b,
                  dictionary)
      alignment = Alignment(multilingual_document)
      for match in DynamicAlign(
                multilingual_document,
                lang_a,
                lang_b,
                sentence_baselines,
                get_match_probability,
                self._min_match_probability,
                dictionary):
        alignment.AddMatch(match)
      del sentence_baselines
      return alignment

    get_match_probability = \
        lambda lang_a, sent_a, lang_b, sent_b, dictionary, num_a, num_b: \
            self.GetMatchProbabilityMultipleSentences(
                multilingual_document,
                lang_a, sent_a, num_a,
                lang_b, sent_b, num_b,
                dictionary)
    alignments = {}
    match_fu = FindUnion()
    if self._pivot_operand == 'OR':
      if self._pivot_size == 0:
        for lang_a, lang_b in EnumeratePairs(languages):
          for match in DynamicAlign(
              multilingual_document,
              lang_a,
              lang_b,
              sentence_baselines,
              get_match_probability,
              self._min_match_probability,
              dictionary):
            match_fu.AddIfNotExists(*match)
            match_fu.Union(*match)
      else:
        pivot = languages[:self._pivot_size]
        for lang_a in languages:
          if lang_a in pivot:
            continue
          for lang_b in pivot:
            for match in DynamicAlign(
                multilingual_document,
                lang_a,
                lang_b,
                sentence_baselines,
                get_match_probability,
                self._min_match_probability,
                dictionary):
              match_fu.AddIfNotExists(*match)
              match_fu.Union(*match)
      matches = {}
      for key in match_fu:
        root = match_fu.Find(key)
        if not root in matches:
          matches[root] = []
        matches[root].append(key)
    else:
        assert(False)

    alignment = Alignment(multilingual_document)
    for match in matches.values():
      alignment.AddMatch(match)
    del match_fu
    del sentence_baselines
    return alignment

