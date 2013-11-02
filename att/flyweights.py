import nltk

class FlyweightFactory(object):
  def __init__(self, constructor):
    self._cache = {}
    self._constructor = constructor

  def GetOrMake(self, name):
    if name not in self._cache:
      self._cache[name] = self._constructor(name)
    return self._cache[name]
nltk_tokenizer_flyweight_factory = FlyweightFactory(
    lambda language: nltk.data.load('tokenizers/punkt/%s.pickle' % language))
