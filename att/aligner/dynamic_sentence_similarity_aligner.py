from sentence_similarity_aligner import SentenceSimilarityAligner
from aligner_factory import AlignerFactory
from att.alignment import Alignment

def DynamicAlign(multilingual_document,
                 lang_a,
                 lang_b,
                 sentence_baselines,
                 get_match_probability,
                 min_match_probability,
                 dictionary,
                 max_num_consecutive_sentences=3):
  class Dir(object):
    A_SKIP, B_SKIP, MATCH = xrange(3)

  def GetQuality(dpdata, i, j):
    if i >= 0 and j >= 0:
      if dpdata[i][j] is not None and dpdata[i][j][0] is not None:
        return dpdata[i][j][0]
    return 0

  assert lang_a in multilingual_document.GetLanguages()
  assert lang_b in multilingual_document.GetLanguages()

  sentences_a = multilingual_document.GetSentences(lang_a)
  sentences_b = multilingual_document.GetSentences(lang_b)
  # dpdata[A][B] is a pair: (quality, direction, num_sentences_a_aligned, num_sentences_b_aligned).
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

  # A table, filled during alignment, containing the largest sentence in a and b text
  # filled so far
  allowed_sentence_id = [[(-1, -1) for unused_sentenceB in xrange(len(sentences_b))]
                                   for unused_sentenceA in xrange(len(sentences_a))]

  # Maximal % of sentence number we can go away from the diagonal
  if len(sentences_a) < 10 or len(sentences_b) < 10:
    max_diff = 1
  else:
    max_diff = 1

  for sent_a in  xrange(len(sentences_a)):
    for sent_b in  xrange(len(sentences_b)):
      # if we are too far from the diagonal, exit (with implied 0)
      #
      # diff = abs(float(sent_a) / len(sentences_a) - float(sent_b) / len(sentences_b))
      # if diff > max_diff:
      #   continue 

      quality_a_skip = GetQuality(dpdata, sent_a - 1, sent_b)
      quality_b_skip = GetQuality(dpdata, sent_a, sent_b - 1)
      max_quality = 0
      for a_i in range(1, max_num_consecutive_sentences + 1):
        for b_i in range(1, max_num_consecutive_sentences + 1):
          if a_i > sent_a or b_i > sent_b:
            continue

          allowed_a, allowed_b = allowed_sentence_id[sent_a - a_i][sent_b - b_i]

#          if sent_a - a_i <= allowed_a or sent_b - b_i <= allowed_b:
#            continue

          match_baseline = sentence_baselines[(lang_a, sent_a - a_i, a_i)] * \
                           sentence_baselines[(lang_b, sent_b - b_i, b_i)]
          match_probability = get_match_probability(
                                  lang_a,
                                  sent_a - a_i,
                                  lang_b,
                                  sent_b - b_i,
                                  dictionary,
                                  a_i,
                                  b_i)
          quality_match = GetQuality(dpdata, sent_a - a_i, sent_b - b_i) + \
                          match_probability * match_probability / match_baseline
          if match_probability * match_probability / match_baseline >= \
               min_match_probability and quality_match > max_quality:
            max_quality = max(max_quality, quality_match)
            dpdata[sent_a][sent_b] = (quality_match, Dir.MATCH, a_i, b_i)
            allowed_sentence_id[sent_a][sent_b] = (sent_a, sent_b)
      if quality_b_skip > max_quality:
        max_quality = quality_b_skip
        dpdata[sent_a][sent_b] = (quality_b_skip, Dir.B_SKIP, None, None)
        allowed_sentence_id[sent_a][sent_b] = allowed_sentence_id[sent_a][sent_b - 1]
      elif quality_a_skip >= max_quality:
        max_quality = quality_a_skip
        dpdata[sent_a][sent_b] = (quality_a_skip, Dir.A_SKIP, None, None)
        allowed_sentence_id[sent_a][sent_b] = allowed_sentence_id[sent_a - 1][sent_b]

  sent_a = len(sentences_a) - 1
  sent_b = len(sentences_b) - 1
  matches = []
  while sent_a >= 0 and sent_b >= 0:
#    diff = abs(float(sent_a) / len(sentences_a) - float(sent_b) / len(sentences_b))
#    if diff > max_diff:
#      if float(sent_a) / len(sentences_a) >  float(sent_b) / len(sentences_b):
#        sent_a -= 1
#      else:
#        sent_b -= 1
#      continue

    unused_quality, direction, num_sent_a, num_sent_b = dpdata[sent_a][sent_b]
    if direction == Dir.MATCH:
      match = []
      for a_i in range(0, num_sent_a):
        match.append((lang_a, sent_a - a_i))
      for b_i in range(0, num_sent_b):
        match.append((lang_b, sent_b - b_i))
      matches.append(match)
      sent_a -= num_sent_a
      sent_b -= num_sent_b
    elif direction == Dir.A_SKIP:
      sent_a -= 1
    else:  # direction == Dir.B_SKIP
      sent_b -= 1
  del dpdata
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
    sentence_baselines = self._CalculateSentenceBaselines(
        multilingual_document,
        dictionary)
    get_match_probability = \
            lambda lang_a, sent_a, lang_b, sent_b, dictionary, num_a, num_b: \
                self.GetMatchProbabilityMultipleSentences(
                    multilingual_document,
                    lang_a, sent_a, num_a,
                    lang_b, sent_b, num_b,
                    dictionary)
    matches = DynamicAlign(multilingual_document,
                           lang_a,
                           lang_b,
                           sentence_baselines,
                           get_match_probability,
                           self._min_match_probability,
                           dictionary)
    alignment = Alignment(multilingual_document)
    for match in reversed(matches):
      alignment.AddMatch(match)
    return alignment
