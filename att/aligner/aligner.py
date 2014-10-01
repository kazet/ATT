from att.utils import Average, StandardDeviation, GetStatisticsString
from att.log import LogDebug
from att.eta_clock import ETAClock

class Aligner(object):
  def __init__(self, config={}):
    pass

  def Align(self, multilingual_document):
    raise NotImplementedError()

  def Train(self, training_corpus, training_set_size):
    pass

  def Verify(self, alignment, dictionary):
    return 0


  def Evaluate(self, test_corpus, dictionary):
    identifiers = list(test_corpus.GetMultilingualDocumentIdentifiers())
    eta_clock = ETAClock(0, len(identifiers), "Evaluating aligner")
    precisions = []
    recalls = []
    f_measures = []
    verifications = []
    for identifier in identifiers:
      reference_alignment = test_corpus.GetMultilingualAlignedDocument(identifier)
      our_alignment = self.Align(
          reference_alignment.GetMultilingualDocument(),
          dictionary)
      evaluation = our_alignment.Evaluate(reference_alignment)
      eta_clock.Tick()

      verification = self.Verify(our_alignment, dictionary)
      verifications.append(verification)

      precisions.append(evaluation['precision'])
      recalls.append(evaluation['recall'])
      f_measures.append(evaluation['f_measure'])

      LogDebug("Current document: precision %.3f recall %.3f f-measure %.3f verification %.3f\n",
               evaluation['precision'],
               evaluation['recall'],
               evaluation['f_measure'],
               verification)
      LogDebug("Precision so far: %s\n"
               "Recall so far: %s\n"
               "F-measure so far: %s\n"
               "Verifications so far: %s\n",
               GetStatisticsString(precisions),
               GetStatisticsString(recalls),
               GetStatisticsString(f_measures),
               GetStatisticsString(verifications))
    return {'avg_precision': Average(precisions),
            'avg_recall': Average(recalls),
            'avg_f_measure': Average(f_measures),
            'avg_verifications': Average(verifications),
            'std_dev_precision': StandardDeviation(precisions),
            'std_dev_recall': StandardDeviation(recalls),
            'std_dev_f_measure': StandardDeviation(f_measures),
            'std_dev_verifications': StandardDeviation(verifications)}
