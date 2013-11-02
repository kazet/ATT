"""See: `Subclassing conventions', `Dictionaries' in the documentation."""

from att.factory import BaseFactory

class DictionaryFactory(BaseFactory):
  """A factory of supported dictionaries. See BaseFactory documentation."""
  CLASSES = {}
