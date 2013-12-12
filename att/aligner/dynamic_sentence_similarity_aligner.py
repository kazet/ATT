from sentence_similarity_aligner import SentenceSimilarityAligner
from aligner_factory import AlignerFactory
from att.alignment import Alignment

def DynamicAlign(lang_a,
                 sentences_a,
                 lang_b,
                 sentences_b,
                 sentence_baselines,
                 get_match_probability,
                 min_match_probability,
                 dictionary):
  class Dir(object):
    A_SKIP, B_SKIP, MATCH = xrange(3)

  def GetQuality(dpdata, i, j):
    if i >= 0 and j >= 0:
      assert dpdata[i][j] is not None
      assert dpdata[i][j][0] is not None
      return dpdata[i][j][0]
    else:
      return 0

  # dpdata[A][B] is a pair: (quality, direction).
  # Quality: the quality of the best alignment of two subdocuments,
  #          sentences[lang_a][:A] and sentences[lang_b][:B]
  #
  # Direction:
  #     Dir.A_SKIP if the best alignment is the same as the best alignment
  #                of sentences[lang_a][:A-1] and sentences[lang_b][:B].
  #     Dir.B_SKIP if the best alignment is the same as the best alignment
  #                of sentences[lang_a][:A] and sentences[lang_b][:B-1].
  #     Dir.MATCH if the best alignment consists of a match, (A, B) and the
  #               best alignment sentences[lang_a][:A-1] and
  #               sentences[lang_b][:B-1].
  dpdata = [[None for unused_sentenceB in xrange(len(sentences_b))]
            for unused_sentenceA in xrange(len(sentences_a))]

  for sent_a in  xrange(len(sentences_a)):
    for sent_b in  xrange(len(sentences_b)):
      match_baseline = sentence_baselines[(lang_a, sent_a)] * \
                       sentence_baselines[(lang_b, sent_b)]
      match_probability = get_match_probability(
                              lang_a,
                              sent_a,
                              lang_b,
                              sent_b,
                              dictionary)
      quality_a_skip = GetQuality(dpdata, sent_a - 1, sent_b)
      quality_b_skip = GetQuality(dpdata, sent_a, sent_b - 1)
      quality_match = GetQuality(dpdata, sent_a - 1, sent_b - 1) + \
                      match_probability * match_probability / match_baseline
      if match_probability * match_probability / match_baseline >= \
              min_match_probability and \
          quality_match > quality_b_skip and \
          quality_match > quality_a_skip:
        dpdata[sent_a][sent_b] = (quality_match, Dir.MATCH)
      elif quality_b_skip > quality_a_skip:
        dpdata[sent_a][sent_b] = (quality_b_skip, Dir.B_SKIP)
      else:  # quality_a_skip >= quality_b_skip
        dpdata[sent_a][sent_b] = (quality_a_skip, Dir.A_SKIP)

  sent_a = len(sentences_a) - 1
  sent_b = len(sentences_b) - 1
  matches = []
  while sent_a >= 0 and sent_b >= 0:
    unused_quality, direction = dpdata[sent_a][sent_b]
    if direction == Dir.MATCH:
      match = [(lang_a, sent_a), (lang_b, sent_b)]
      matches.append(match)
      sent_a -= 1
      sent_b -= 1
    elif direction == Dir.A_SKIP:
      sent_a -= 1
    else:  # direction == Dir.B_SKIP
      sent_b -= 1
  return matches

@AlignerFactory.Register
class DynamicSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(DynamicSentenceSimilarityAligner, self).__init__(config)
    self._min_match_probability = config.get('min_match_probability', 0)

  def Align(self, multilingual_document, dictionary):
    if len(self._languages) != 2:
      raise Exception("DynamicSentenceSimilarityAligner can be used only for"
                      " two languages.")
    self._ResetSignalCaches()

    lang_a = self._languages[0]
    lang_b = self._languages[1]
    sentence_baselines = self._CalculateSentenceBaselines(multilingual_document)
    get_match_probability = \
        lambda lang_a, sent_a, lang_b, sent_b, dictionary: \
            self.GetMatchProbability(
                multilingual_document,
                lang_a, sent_a,
                lang_b, sent_b,
                dictionary)
    matches = DynamicAlign(lang_a,
                           multilingual_document.GetSentences(lang_a),
                           lang_b,
                           multilingual_document.GetSentences(lang_b),
                           sentence_baselines,
                           get_match_probability,
                           self._min_match_probability,
                           dictionary)
    alignment = Alignment(multilingual_document)
    for match in reversed(matches):
      alignment.AddMatch(match)
    return alignment
