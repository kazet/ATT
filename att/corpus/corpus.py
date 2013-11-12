class Corpus(object):
  def GetMultilingualDocument(self, identifier):
    raise NotImplementedError()

  def GetMultilingualDocumentIdentifiers(self):
    raise NotImplementedError()

  def GetFirstIdentifiers(self, num):
    return list(self.GetMultilingualDocumentIdentifiers())[:num]

  def GetMultilingualDocuments(self):
    for identifier in self.GetMultilingualDocumentIdentifiers():
      yield self.GetMultilingualDocument(identifier)

  def GetMultilingualAlignedDocument(self, identifier):
    raise NotImplementedError("This is not an aligned corpus.")
