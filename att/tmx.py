import lxml
import lxml.etree

from att.log import LogDebug
from att.alignment import Alignment
from att.document import Document
from att.language import Languages
from att.multilingual_document import MultilingualDocument

def LoadTMXAlignedDocument(identifier, languages):
  LogDebug("[LoadTMXAlignedDocument] loading %s", identifier)
  data = ''.join(open(identifier).readlines())

  documents = dict([(lang, Document([], lang)) for lang in languages])

  matches = []
  sentences = lxml.etree.fromstring(data).xpath("//tu")
  i = 0
  scores = {}
  for sentence in sentences:
    match = []
    for score in sentence.xpath('prop[@type="Score"]'):
      scores[i] = float(score.text) if score.text != 'None' else None
    for translation in sentence.xpath("tuv"):
      lang = Languages.FromLangRegionCode(translation.get('lang'))
      if lang and lang in languages:
        content = translation.xpath("string()")
    
        match.append( (lang, documents[lang].NumSentences()) )
        documents[lang].AddSentence(unicode(content))
    if len(match):
      matches.append(match)
      i += 1

  multilingual_document = MultilingualDocument(documents.values())
  result = Alignment(multilingual_document, matches)

  for i, score in scores.items():
    result.SetScore(i, score)
  return result

