from aligner_factory import AlignerFactory
from dynamic_sentence_similarity_aligner import DynamicAlign
from sentence_similarity_aligner import SentenceSimilarityAligner

from att.log import LogDebug
from att.alignment import Alignment
from att.find_union import FindUnion
from att.utils import EnumeratePairs

@AlignerFactory.Register
class CombinedDynamicSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(CombinedDynamicSentenceSimilarityAligner, self).__init__(config)
    self._min_match_probability = config.get('min_match_probability', 0)
    self._pivot_operand = config.get('pivot_operand', 'AND')
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

    get_match_probability = \
        lambda lang_a, sent_a, lang_b, sent_b, dictionary: \
            self.GetMatchProbability(
                multilingual_document,
                lang_a, sent_a,
                lang_b, sent_b,
                dictionary)
    alignments = {}
    match_fu = FindUnion()
    if self._pivot_size == 0:
      for lang_a, lang_b in EnumeratePairs(self._languages):
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
      pivot = self._languages[:self._pivot_size]
      if self._pivot_operand == 'AND':
        raise NotImplementedError()
      elif self._pivot_operand == 'OR':
        for lang_a in self._languages:
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
      else:
        assert(False)

    matches = {}
    for key in match_fu:
      root = match_fu.Find(key)
      if not root in matches:
        matches[root] = []
      matches[root].append(key)

    alignment = Alignment(multilingual_document)
    for match in matches.values():
      alignment.AddMatch(match)
    return alignment

