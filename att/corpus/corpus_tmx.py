import os
import lxml
import lxml.etree
from att.log import LogDebug
from corpus import Corpus
from att.document import Document
from att.alignment import Alignment
from att.multilingual_document import MultilingualDocument
from att.language import Languages
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class CorpusTMX(Corpus):
  """Corpus in TMX format."""
  ALL_LANGUAGES = ['en', 'de', 'es', 'pl']

  def __init__(self, config):
    LogDebug("[CorpusTMX] initialization...")
    self._languages = Languages.GetMultipleByCode(
        config.get('languages', CorpusTMX.ALL_LANGUAGES))
    LogDebug("[CorpusTMX] languages: %s",
             ', '.join(map(str, self._languages)))
    self._config_dir = config.get('runtime', {}).get('config_dir', '')
    self._identifiers_file = os.path.join(self._config_dir,
                                          config['identifiers_file'])
    self._data_location = os.path.join(self._config_dir,
                                       config['data_location'])
    LogDebug("[CorpusTMX] initialization finished")

  def GetMultilingualDocumentIdentifiers(self):
    for line in open(self._identifiers_file):
      yield line.strip()

  def GetMultilingualDocument(self, identifier):
    return self \
        .GetMultilingualAlignedDocument(identifier) \
        .GetMultilingualDocument()

  def GetMultilingualAlignedDocument(self, identifier):
    data = '' \
      .join(open(os.path.join(self._data_location, '%s' % identifier)) \
      .readlines())

    documents = dict([(lang, Document([], lang)) for lang in self._languages])

    matches = []
    sentences = lxml.etree.fromstring(data).xpath("//tu")
    for sentence in sentences:
      match = []
      for translation in sentence.xpath("tuv"):
        lang = Languages.FromLangRegionCode(translation.get('lang'))
        if lang and lang in self._languages:
          content = translation.xpath("string()")
      
          match.append( (lang, documents[lang].NumSentences()) )
          documents[lang].AddSentence(unicode(content))
      if len(match):
        matches.append(match)

    multilingual_document = MultilingualDocument(documents.values())
    result = Alignment(multilingual_document, matches)
    return result

