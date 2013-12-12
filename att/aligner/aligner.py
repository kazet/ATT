from att.utils import Average
from att.eta_clock import ETAClock

class Aligner(object):
  def Align(self, multilingual_document):
    raise NotImplementedError()

  def Train(self, training_corpus, training_set_size):
    pass

  def Evaluate(self, test_corpus, dictionary):
    identifiers = list(test_corpus.GetMultilingualDocumentIdentifiers())
    eta_clock = ETAClock(0, len(identifiers), "Evaluating aligner")
    evaluations = []
    for identifier in identifiers:
      reference_alignment = test_corpus.GetMultilingualAlignedDocument(identifier)
      our_alignment = self.Align(
          reference_alignment.GetMultilingualDocument(),
          dictionary)
      evaluations.append(our_alignment.Evaluate(reference_alignment))
      eta_clock.Tick()

    return {'avg_precision': Average([evaluation['precision']
                                      for evaluation in evaluations]),
            'avg_recall': Average([evaluation['recall']
                                   for evaluation in evaluations]),
            'avg_f_measure': Average([evaluation['f_measure']
                                      for evaluation in evaluations])}
