import lxml
import lxml.etree

from att.alignment import Alignment
from att.document import Document
from att.language import Languages
from att.multilingual_document import MultilingualDocument

def LoadTMXAlignedDocument(identifier, languages):
  data = ''.join(open(identifier).readlines())

  documents = dict([(lang, Document([], lang)) for lang in languages])

  matches = []
  sentences = lxml.etree.fromstring(data).xpath("//tu")
  for sentence in sentences:
    match = []
    for translation in sentence.xpath("tuv"):
      lang = Languages.FromLangRegionCode(translation.get('lang'))
      if lang and lang in languages:
        content = translation.xpath("string()")
    
        match.append( (lang, documents[lang].NumSentences()) )
        documents[lang].AddSentence(unicode(content))
    if len(match):
      matches.append(match)

  multilingual_document = MultilingualDocument(documents.values())
  result = Alignment(multilingual_document, matches)
  return result

