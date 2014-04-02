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
    self._pivot_operand = config.get('pivot_operand', 'AND')
    self._pivot_size = config.get('pivot_size', 0)
    LogDebug("[CombinedDynamicSentenceSimilarityAligner] "
             "pivot_operand=%s pivot_size=%d min_match_probability=%.3f",
             self._pivot_operand,
             self._pivot_size,
             self._min_match_probability)

  def Align(self, multilingual_document, dictionary, ready_sentence_baselines=None):
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
          lambda lang_a, sent_a, lang_b, sent_b, dictionary: \
              self.GetMatchProbability(
                  multilingual_document,
                  lang_a, sent_a,
                  lang_b, sent_b,
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
      return alignment

    self._ResetSignalCaches()
    self._pivot_operand = 'OR'
    self._pivot_size = 2

    get_match_probability = \
        lambda lang_a, sent_a, lang_b, sent_b, dictionary: \
            self.GetMatchProbability(
                multilingual_document,
                lang_a, sent_a,
                lang_b, sent_b,
                dictionary)
    alignments = {}
    match_fu = FindUnion()
    pivot = languages[:self._pivot_size]
    if self._pivot_operand == 'MID':
        matches = {}
        for lang_a in languages:
          for lang_b in languages:
            if lang_b == lang_a:
              continue
            matches[(lang_a, lang_b)] = []
            for match in DynamicAlign(
                multilingual_document,
                lang_a,
                lang_b,
                sentence_baselines,
                get_match_probability,
                self._min_match_probability,
                dictionary):
              if match[0][0] == lang_a:
                assert match[1][0] == lang_b
                matches[(lang_a, lang_b)].append([match[0], match[1]])
              else:
                assert match[0][0] == lang_b
                assert match[1][0] == lang_a
                matches[(lang_a, lang_b)].append([match[1], match[0]])

        match_scores = {}
        for lang_a in languages:
          for lang_b in languages:
            if lang_b == lang_a:
              continue
            for lang_c in languages:
              if lang_b == lang_c or lang_a == lang_c:
                continue
              for acmatch in matches[(lang_a, lang_c)]:
                assert acmatch[0][0] == lang_a
                assert acmatch[1][0] == lang_c

                asid = acmatch[0][1]
                csid_1 = acmatch[1][1]
                for bcmatch in matches[(lang_b, lang_c)]:
                  assert bcmatch[0][0] == lang_b
                  assert bcmatch[1][0] == lang_c

                  bsid = bcmatch[0][1]
                  csid_2 = bcmatch[1][1]
                  if csid_1 == csid_2:
                    if not (lang_a, asid, lang_b, bsid) in match_scores:
                      match_scores[(lang_a, asid, lang_b, bsid)] = 0
                    match_scores[(lang_a, asid, lang_b, bsid)] += 1
        for (lang_a, sid_a, lang_b, sid_b), score in match_scores.iteritems():
          if score > self._pivot_size:
            match_fu.AddIfNotExists( (lang_a, sid_a,) )
            match_fu.AddIfNotExists( (lang_b, sid_b,) )
            match_fu.Union((lang_a, sid_a,), (lang_b, sid_b,))
        matches = {}
        for key in match_fu:
          root = match_fu.Find(key)
          if not root in matches:
            matches[root] = []
          matches[root].append(key)
    elif self._pivot_operand == 'AND':
      all_graph_edges = []
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
          all_graph_edges.append(match)
      connected_subgraphs = {}
      for edge in all_graph_edges:
        assert len(edge) == 2
        root = match_fu.Find(edge[0])
        root2 = match_fu.Find(edge[1])
        assert root == root2
        if not root in connected_subgraphs:
          connected_subgraphs[root] = []
        connected_subgraphs[root].append(tuple(edge))
      matches = {}
      for key in connected_subgraphs.keys():
        if len(connected_subgraphs[key]) < len(languages) * 2:
          matches[key] = MaxClique(connected_subgraphs[key])
        else:
          # co tu sie dzieje
          matches[key] = sorted(connected_subgraphs[key])[:len(languages) * 2]
          # TODO: we can't use the exact version of MaxClique here
    elif self._pivot_operand == 'OR':
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
    return alignment

