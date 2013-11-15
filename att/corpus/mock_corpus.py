from corpus import Corpus
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class MockCorpus(Corpus):
  def __init__(self, config):
    mdocs = []
    self._identifiers = []
    for mdoc in config['multilingual_documents']:
      # we want to preserve order
      self._identifiers.append(mdoc['identifier'])
      mdocs.append( (mdoc['identifier'], mdoc['multilingual_document']) )
    self._languages = config.get('languages', [])
    self._mdoc_dict = dict(mdocs)

  def GetMultilingualDocument(self, identifier):
    return self._mdoc_dict[identifier]

  def GetMultilingualDocumentIdentifiers(self):
    return self._identifiers
