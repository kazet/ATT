"""See `SentenceSimilarityAligner: available signals', `Subclassing
conventions' in the documentation."""

from att.factory import BaseFactory

class SignalFactory(BaseFactory):
  """A factory of supported sentence similarity signals. See BaseFactory
  documentation."""
  CLASSES = {}
