import os

class SignalsInitialBucketValueCollection(object):
  """Stores the default signal bucket values (without any training performed)
  created by smoothing from data returned by different training."""
  DEFAULT_BUCKET_VALUES_REPR = \
      open(os.path.join(os.path.dirname(__file__),
                        'signals_initial_bucket_values')).read()

  def __init__(self, bucket_values_repr=None):
    if not bucket_values_repr:
      self._bucket_values_repr = SignalsInitialBucketValueCollection.DEFAULT_BUCKET_VALUES_REPR
    else:
      self._bucket_values_repr = bucket_values_repr
    self._bucket_values = {}
    for record in self._bucket_values_repr.split('|'):
      tokens = record.split(' ')
      signal_name = tokens[0]
      self._bucket_values[signal_name] = [float(token) for token in tokens[1:]]

  def GetBucketValuesFor(self, signal_name):
    return self._bucket_values[signal_name]

  def HasBucketValuesFor(self, signal_name):
    return signal_name in self._bucket_values
