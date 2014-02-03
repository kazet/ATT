import os
from att.log import LogDebug
from corpus import Corpus
from att.multilingual_document import MultilingualDocument
from att.language import Languages
from att.tmx import LoadTMXAlignedDocument
from att.utils import RecursiveListing, HasExtension
from corpus_factory import CorpusFactory

@CorpusFactory.Register
class CorpusTMX(Corpus):
  """Corpus in TMX format."""
  def __init__(self, config):
    LogDebug("[CorpusTMX] initialization...")
    self._languages = Languages.GetMultipleByCode(config['languages'])
    LogDebug("[CorpusTMX] languages: %s",
             ', '.join(map(str, self._languages)))
    self._config_dir = config.get('runtime', {}).get('config_dir', '')
    self._data_location = os.path.join(self._config_dir,
                                       config['data_location'])
    self._identifiers = [
        filename
        for filename in RecursiveListing(self._data_location)
        if HasExtension(filename, '.tmx')]
    LogDebug("[CorpusTMX] initialization finished")

  def GetMultilingualDocumentIdentifiers(self):
    return self._identifiers

  def GetMultilingualDocument(self, identifier):
    return self \
        .GetMultilingualAlignedDocument(identifier) \
        .GetMultilingualDocument()

  def GetMultilingualAlignedDocument(self, identifier):
    return LoadTMXAlignedDocument(identifier, self._languages)
