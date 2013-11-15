from att import log
from corpus import Corpus
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class CorpusUnion(Corpus):
  """Sum of two or more corpora."""

  def __init__(self, config):
    if 'runtime' in config:
      for corpus in config['corpora']:
        corpus['runtime'] = config['runtime']
    self._corpora = [CorpusFactory.Make(corpus)
                     for corpus in config['corpora']]
    self._languages = self._corpora[0].GetLanguages()
    for corpus in self._corpora:
      if set(corpus.GetLanguages()) != set(self._languages):
        raise Exception("Language sets of all corpora in CorpusUnion should be the same")
    corpora_names = [corpus.__class__.__name__ for corpus in self._corpora]

  def GetMultilingualDocumentIdentifiers(self):
    i = 0
    for corpus in self._corpora:
      for identifier in corpus.GetMultilingualDocumentIdentifiers():
        yield "%s_%s" % (i, identifier)
      i += 1

  def GetMultilingualAlignedDocument(self, identifier_pack):
    corpus_id, identifier = self._UnpackIdentifier(identifier_pack)
    return self._corpora[corpus_id].GetMultilingualAlignedDocument(identifier)

  def GetMultilingualDocument(self, identifier_pack):
    corpus_id, identifier = self._UnpackIdentifier(identifier_pack)
    return self._corpora[corpus_id].GetMultilingualDocument(identifier)

  def _UnpackIdentifier(self, identifier_pack):
    parts = identifier_pack.split('_')
    corpus_id = int(parts[0])
    identifier = '_'.join(parts[1:])
    return corpus_id, identifier
