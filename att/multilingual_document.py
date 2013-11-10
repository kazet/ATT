class MultilingualDocument(object):
  def __init__(self, documents):
    self._document_dict = dict([(doc.GetLanguage(), doc) for doc in documents])

  def __str__(self):
    return '\n'.join(["[%s] %s" % (lang, doc)
                      for lang, doc in self._document_dict.iteritems()])

  def GetLanguages(self):
    return self._document_dict.keys()

  def GetDocuments(self):
    return self._document_dict

  def GetDocument(self, language):
    return self._document_dict[language]

  def GetSentence(self, language, i):
    return self._document_dict[language].GetSentence(i)

  def GetSentences(self, language):
    return self._document_dict[language].GetSentences()

  def NumSentences(self, language):
    return self._document_dict[language].NumSentences()

  def GetDocumentOrNone(self, language):
    if language in self._document_dict:
      return self._document_dict[language]
    else:
      return None
