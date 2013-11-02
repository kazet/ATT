from att.utils import Average

class Aligner(object):
  def Align(self, multilingual_document):
    raise NotImplementedError()

  def Train(self, training_corpus):
    pass

  def Evaluate(self, test_corpus):
    evaluations = []
    for identifier in test_corpus.GetMultilingualDocumentIdentifiers():
      reference_alignment = test_corpus.GetMultilingualAlignedDocument(identifier)
      our_alignment = self.Align(reference_alignment.GetMultilingualDocument())
      evaluations.append(our_alignment.Evaluate(reference_alignment))

    return {'avg_precision': Average([evaluation['precision']
                                      for evaluation in evaluations]),
            'avg_recall': Average([evaluation['recall']
                                   for evaluation in evaluations]),
            'avg_f_measure': Average([evaluation['f_measure']
                                      for evaluation in evaluations])}
