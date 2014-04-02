import lxml
import lxml.html
from att import flyweights
from att.utils import Flatten


class Document(object):
  """Represents a list of sentences."""
  def __init__(self, sentences, language):
    self._sentences = sentences
    self._language = language

  def __str__(self):
    return '/'.join(self._sentences)

  def __repr__(self):
    return self.__str__()

  def __unicode__(self):
    return self.__str__()

  def NumSentences(self):
    return len(self._sentences)

  def AddSentence(self, sentence):
    self._sentences.append(sentence)

  def GetSentences(self):
    return self._sentences

  def GetSentence(self, i):
    if i >= len(self._sentences):
      return ""
    return self._sentences[i]

  def GetLanguage(self):
    return self._language


class DocumentFactory(object):
  @staticmethod
  def MakeFromHTMLParagraphList(html, language, tag='p'):
    """Each sentence is contained in a separate paragraph."""
    tree = lxml.html.fromstring(html)
    paragraphs = [element.text for element in tree.findall('.//%s' % tag)]
    tokenizer = flyweights.nltk_tokenizer_flyweight_factory.GetOrMake(language.GetNLTKName())
    sentences = Flatten([tokenizer.tokenize(paragraph) for paragraph in paragraphs])
    return Document(sentences, language)
