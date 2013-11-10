import math

from sentence_similarity_aligner import SentenceSimilarityAligner
from sentence_similarity_signals import SignalFactory
from aligner_factory import AlignerFactory
from att.alignment import Alignment
from att.global_context import global_context
from att.log  import VerboseLevel, LogDebugFull
from att.classifier.signal_aggregator import TuneWeights
from att.classifier import LinearRegression, FastBucketAverage
from att.eta_clock import ETAClock
from att.utils import EnumeratePairs, Average
from att.language import Languages
from att.log import LogDebug

@AlignerFactory.Register
class DynamicSentenceSimilarityAligner(SentenceSimilarityAligner):
  def __init__(self, config):
    super(DynamicSentenceSimilarityAligner, self).__init__(config)
    self._min_match_probability = config.get('min_match_probability', 2)

  def Align(self, multilingual_document):
    class Dir(object):
      A_SKIP, B_SKIP, MATCH = xrange(3)

    def GetQuality(dpdata, i, j):
      if i >= 0 and j >= 0:
        assert dpdata[i][j] is not None
        assert dpdata[i][j][0] is not None
        return dpdata[i][j][0]
      else:
        return 0

    if len(self. _languages) != 2:
      raise Exception("DynamicSentenceSimilarityAligner can be used only for"
                      " two languages.")
    langA = self._languages[0]
    langB = self._languages[1]
    sentence_baselines = self._CalculateSentenceBaselines(multilingual_document)
    alignment = Alignment(multilingual_document)
    # dpdata[A][B] is a pair: (quality, direction).
    # Quality: the quality of the best alignment of two subdocuments,
    #          sentences[langA][:A] and sentences[langB][:B]
    #
    # Direction:
    #     Dir.A_SKIP if the best alignment is the same as the best alignment
    #                of sentences[langA][:A-1] and sentences[langB][:B].
    #     Dir.B_SKIP if the best alignment is the same as the best alignment
    #                of sentences[langA][:A] and sentences[langB][:B-1].
    #     Dir.MATCH if the best alignment consists of a match, (A, B) and the
    #               best alignment sentences[langA][:A-1] and
    #               sentences[langB][:B-1].
    dpdata = [[None for unused_sentenceB
                    in xrange(multilingual_document.NumSentences(langB))]
              for unused_sentenceA
              in xrange(multilingual_document.NumSentences(langA))]

    for sentA in xrange(multilingual_document.NumSentences(langA)):
      for sentB in xrange(multilingual_document.NumSentences(langB)):
        match_baseline = sentence_baselines[(langA, sentA)] * \
                         sentence_baselines[(langB, sentB)]
        match_probability = self.GetMatchProbability(
                                multilingual_document,
                                langA,
                                sentA,
                                langB,
                                sentB)
        quality_a_skip = GetQuality(dpdata, sentA - 1, sentB)
        quality_b_skip = GetQuality(dpdata, sentA, sentB - 1)
        quality_match = GetQuality(dpdata, sentA - 1, sentB - 1) + \
                        match_probability / match_baseline
        if match_probability * match_probability / match_baseline >= self._min_match_probability and \
            quality_match > quality_b_skip and \
            quality_match > quality_a_skip:
          dpdata[sentA][sentB] = (quality_match, Dir.MATCH)
        elif quality_b_skip > quality_a_skip:
          dpdata[sentA][sentB] = (quality_b_skip, Dir.B_SKIP)
        else:  # quality_a_skip >= quality_b_skip
          dpdata[sentA][sentB] = (quality_a_skip, Dir.A_SKIP)

    sentA = multilingual_document.NumSentences(langA) - 1
    sentB = multilingual_document.NumSentences(langB) - 1
    matches = []
    while sentA >= 0 and sentB >= 0:
      unused_quality, direction = dpdata[sentA][sentB]
      if direction == Dir.MATCH:
        match = [(langA, sentA), (langB, sentB)]
        matches.append(match)
        sentA -= 1
        sentB -= 1
      elif direction == Dir.A_SKIP:
        sentA -= 1
      else:  # direction == Dir.B_SKIP
        sentB -= 1

    for match in reversed(matches):
      alignment.AddMatch(match)
    return alignment
