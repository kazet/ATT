import os
import lxml
import lxml.html
import yaml
from att.log import LogDebug
from att.url import CachedURL
from att.document import DocumentFactory
from att.multilingual_document import MultilingualDocument
from att.language import Languages
from corpus import Corpus
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class CorpusEurlex(Corpus):
  ALL_LANGUAGES = ['en', 'de', 'es', 'pl']

  def __init__(self, config):
    self._languages = Languages.GetMultipleByCode(
        config.get('languages', CorpusEurlex.ALL_LANGUAGES))
    self._config_dir = config.get('runtime', {}).get('config_dir', '')
    self._identifiers_file = os.path.join(self._config_dir,
                                          config['identifiers_file'])
    self._config = config

  def GetMultilingualDocumentAlignment(self):
    raise NotImplementedError()

  def GetMultilingualDocumentIdentifiers(self):
    for line in open(self._identifiers_file):
      yield line.strip()

  def GetMultilingualDocument(self, identifier):
    def GetDocument(lang):
      data = CachedURL('http://eur-lex.europa.eu/LexUriServ/'
                       'LexUriServ.do?uri=CELEX:%s:%s:HTML' % (identifier,
                                                               lang.GetCode().upper())).get()
      content = lxml.html.fromstring(data).xpath("//txt_te")

      if len(content) == 0:
        return None
      else:
        return DocumentFactory.MakeFromHTMLParagraphList(
            lxml.html.tostring(content[0], pretty_print=True),
            lang)

    documents = []
    for lang in self._languages:
      doc = GetDocument(lang)

      if doc:
        documents.append(doc)

    return MultilingualDocument(documents)
