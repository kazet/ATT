class Corpus(object):
  def GetMultilingualDocument(self, identifier):
    raise NotImplementedError()

  def GetMultilingualDocumentIdentifiers(self):
    raise NotImplementedError()

  def GetMultilingualDocuments(self):
    for identifier in self.GetMultilingualDocumentIdentifiers():
      yield self.GetMultilingualDocument(identifier)

  def GetMultilingualAlignedDocument(self, identifier):
    raise NotImplementedError()
