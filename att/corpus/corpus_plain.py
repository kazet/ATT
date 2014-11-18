import os

from corpus import Corpus
from corpus_factory import CorpusFactory

from att.document import Document
from att.language import Languages
from att.log import LogDebug
from att.multilingual_document import MultilingualDocument

@CorpusFactory.Register
class CorpusPlain(Corpus):
  """Corpus with the following format:
  
  config['data_location'] determines the corpus location (a folder)
  each of the subfolders of the corpus folder represents one multilingual
  document, files in the subfolders represent
  single-language documents (one line per one sentence).
  
  The sentence positions don't mean anything -- this corpus doesn't support
  aligned documents."""

  def __init__(self, config):
    LogDebug("[CorpusPlain] initialization...")
    self._languages = Languages.GetMultipleByCode(config['languages'])
    LogDebug("[CorpusPlain] languages: %s",
             ', '.join(map(str, self._languages)))
    self._config_dir = config.get('runtime', {}).get('config_dir', '')
    self._data_location = os.path.join(self._config_dir,
                                       config['data_location'])
    self._identifiers = [
          folder
          for folder in os.listdir(self._data_location)
          if os.path.isdir(os.path.join(self._data_location, folder))]

    # Limits the corpus to first X documents
    if 'limit' in config:
      self._identifiers = self._identifiers[:config['limit']]

    LogDebug("[CorpusPlain] initialization finished")

  def GetMultilingualDocumentIdentifiers(self):
    return self._identifiers

  def GetMultilingualDocument(self, identifier):
    docs = []
    for language in self._languages:
      document_path = os.path.join(
          self._data_location,
          identifier,
          language.GetCode())
      if not os.path.exists(document_path):
        continue

      sentences = [unicode(sentence, encoding="utf-8", errors="ignore")
                   for sentence in open(document_path).readlines()]
      docs.append(Document(sentences, language))
    return MultilingualDocument(docs)
