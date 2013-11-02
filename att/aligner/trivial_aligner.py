from aligner import Aligner
from aligner_factory import AlignerFactory
from att.alignment import Alignment

@AlignerFactory.Register
class TrivialAligner(Aligner):
  """Aligns first sentences in all languages together, then all second
  sentences together etc."""

  def __init__(self, unused_config):
    pass

  def GetModel(self):
    return {}

  def SetModel(self, model):
    pass

  def Align(self, multilingual_document):
    shortest_document_length = None

    for language in multilingual_document.GetLanguages():
      document = multilingual_document.GetDocument(language)

      if len(document.GetSentences()) < shortest_document_length or \
        shortest_document_length is None:
        shortest_document_length = len(document.GetSentences())

    alignment = Alignment(multilingual_document)
    for i in range(0, shortest_document_length):
      match = []
      for language in multilingual_document.GetLanguages():
        match.append( (language, i,) )
      alignment.AddMatch(match)
    return alignment
