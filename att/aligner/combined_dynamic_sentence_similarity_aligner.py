from sentence_similarity_aligner import SentenceSimilarityAligner
from aligner_factory import AlignerFactory
from att.alignment import Alignment
from att.utils import EnumeratePairs
from dynamic_sentence_similarity_aligner import DynamicAlign
from att.find_union import FindUnion

@AlignerFactory.Register
class CombinedDynamicSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(CombinedDynamicSentenceSimilarityAligner, self).__init__(config)
    self._min_match_probability = config.get('min_match_probability', 0)

  def Align(self, multilingual_document):
    sentence_baselines = self._CalculateSentenceBaselines(multilingual_document)
    get_match_probability = \
        lambda lang_a, sent_a, lang_b, sent_b: self.GetMatchProbability(
            multilingual_document, lang_a, sent_a, lang_b, sent_b)

    alignments = {}
    match_fu = FindUnion()
    for lang_a, lang_b in EnumeratePairs(self._languages):
      for match in DynamicAlign(
          lang_a,
          multilingual_document.GetSentences(lang_a),
          lang_b,
          multilingual_document.GetSentences(lang_b),
          sentence_baselines,
          get_match_probability,
          self._min_match_probability):
        match_fu.AddIfNotExists(*match)
        match_fu.Union(*match)

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

