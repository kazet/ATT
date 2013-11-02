"""See `Languages' in the documentation."""

from att.language.language import Language

class Languages(object):
  """The collection of all languages supported."""
  LANGUAGES = {
    'en': Language(code='en', name='English', id=1),
    'de': Language(code='de', name='German', id=2),
    'es': Language(code='es', name='Spanish', id=3),
    'pl': Language(code='pl', name='Polish', id=4)
  }

  @staticmethod
  def FromLangRegionCode(lang_region_code):
    """Convert language region code (i.e. pt-BR) to Language object."""
    lang = lang_region_code.split('-')[0].lower()
    if lang in Languages.LANGUAGES:
      return Languages.GetByCode(lang)
    else:
      return None

  @staticmethod
  def All():
    """Return all languages available."""
    return Languages.LANGUAGES

  @staticmethod
  def GetByCode(code):
    """Convert language code (i.e. `en') to Language object."""
    if code in Languages.LANGUAGES:
      return Languages.LANGUAGES[code]
    else:
      return None

  @staticmethod
  def GetMultipleByCode(codes):
    """Convert language code list (i.e. ['en', 'pl']) to Language objects
    list."""
    return [Languages.LANGUAGES[code] for code in codes]
