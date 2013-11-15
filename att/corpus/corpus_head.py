from att import log
from corpus import Corpus
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class CorpusHead(Corpus):
  """Takes first N documents from a different corpus."""

  def __init__(self, config):
    if 'runtime' in config:
      config['corpus']['runtime'] = config['runtime']

    self._corpus = CorpusFactory.Make(config['corpus'])
    self._languages = self._corpus.GetLanguages()
    self._n = config['n']

  def GetMultilingualDocumentIdentifiers(self):
    i = 0
    for identifier in self._corpus.GetMultilingualDocumentIdentifiers():
      if i < self._n:
        yield identifier
        i += 1
      else:
        break

  def GetMultilingualDocument(self, identifier):
    return self._corpus.GetMultilingualDocument(identifier)

  def GetMultilingualAlignedDocument(self, identifier):
    return self._corpus.GetMultilingualAlignedDocument(identifier)
