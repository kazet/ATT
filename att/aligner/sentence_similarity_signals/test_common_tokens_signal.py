# pylint: disable=R0904,R0921,C0111

from nltk.tokenize import word_tokenize

from att.test import TestCase
from att.language import Languages
from att.aligner.sentence_similarity_signals.common_tokens_signal \
    import CommonTokensSignal

class CommonTokensSignalTestCase(TestCase):
  def testHighSimilarity(self):
    sentence1 = "ABC WTF"
    sentence2 = "ABC WTF"
    en = Languages.GetByCode('en')
    pl = Languages.GetByCode('pl')
    signal = CommonTokensSignal({})
    self.assertAlmostEqual(signal.GetSimilarity(en, sentence1, pl, sentence2),
                           2.0 / (len(word_tokenize(sentence1)) +
                                  len(word_tokenize(sentence2))))

  def testRepetitions(self):
    sentence1 = "WTF WTF WTF"
    sentence2 = "WTF WTF WTF"
    en = Languages.GetByCode('en')
    pl = Languages.GetByCode('pl')
    signal = CommonTokensSignal({})
    self.assertAlmostEqual(signal.GetSimilarity(en, sentence1, pl, sentence2),
                           3.0 / (len(word_tokenize(sentence1)) +
                                  len(word_tokenize(sentence2))))

  def testMediumSimilarity(self):
    sentence1 = "Ich mag WTF"
    sentence2 = "I like WTF"
    en = Languages.GetByCode('en')
    pl = Languages.GetByCode('pl')
    signal = CommonTokensSignal({})
    self.assertAlmostEqual(signal.GetSimilarity(en, sentence1, pl, sentence2),
                           1.0 / (len(word_tokenize(sentence1)) +
                                  len(word_tokenize(sentence2))))

  def testLowSimilarity(self):
    sentence1 = "nicht"
    sentence2 = "verstehen"
    en = Languages.GetByCode('en')
    pl = Languages.GetByCode('pl')
    signal = CommonTokensSignal({})
    self.assertAlmostEqual(signal.GetSimilarity(en, sentence1, pl, sentence2),
                           0.0 / (len(word_tokenize(sentence1)) +
                                  len(word_tokenize(sentence2))))
