"""See `Languages' in the documentation."""

from att.language.language import Language

class LanguageNotFound(Exception):
  pass

class Languages(object):
  """The collection of all languages supported."""
  LANGUAGES = {
    'en': Language(code='en', name='English', id=1),
    'de': Language(code='de', name='German', id=2),
    'es': Language(code='es', name='Spanish', id=3),
    'pt': Language(code='pt', name='Portuguese', id=4),
    'fr': Language(code='fr', name='French', id=5),
    'hu': Language(code='hu', name='Hungarian', id=6),
    'lt': Language(code='lt', name='Lithuanian', id=7),
    'el': Language(code='el', name='Greek', id=8),
    'sv': Language(code='sv', name='Swedish', id=9),
    'pl': Language(code='pl', name='Polish', id=10),
    'lv': Language(code='lv', name='Latvian', id=11),
    'et': Language(code='et', name='Estonian', id=12),
    'it': Language(code='it', name='Italian', id=13),
  }

  @staticmethod
  def FromLangRegionCode(lang_region_code):
    """Convert language region code (i.e. pt-BR) to Language object."""
    lang = lang_region_code.split('-')[0].lower()
    if lang in Languages.LANGUAGES:
      return Languages.GetByCode(lang)
    else:
      raise LanguageNotFound(lang)

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
      raise LanguageNotFound(code)

  @staticmethod
  def GetMultipleByCode(codes):
    """Convert language code list (i.e. ['en', 'pl']) to Language objects
    list."""
    return [Languages.LANGUAGES[code] for code in codes]
