import bisect

from att.utils import Average, GroupByKey

class BucketAggregator(object):
  """Divide data into a number of intervals and aggregate it."""

  def __init__(self,
               num_buckets=10,
               aggregator=Average):
    self._buckets = None
    self._num_buckets = num_buckets
    self._aggregator = aggregator

  def Train(self, data):
    """Detect the intervals and aggregate the data."""
    bucket_size = int(len(data) / float(self._num_buckets))

    bucket = []
    buckets = []

    for group in GroupByKey(data):
      # if we have a lot of values with the same key,
      # advance to the next bucket faster. Else, wait
      # for the bucket to fill
      if (len(group) >= bucket_size and bucket != []) or \
          len(bucket) >= bucket_size:
        if bucket:
          buckets.append(bucket)
          bucket = []
      bucket.extend(group)
    if bucket:
      buckets.append(bucket)

    self._buckets = []
    for bucket in buckets:
      key = bucket[0][0]
      values = [value_ for unused_key, value_ in bucket]
      self._buckets.append( (key, self._aggregator(values) ) )

  def GetBuckets(self):
    """Returns into what intervals the data has been aggregated."""
    return self._buckets

  def Get(self, key):
    """Returns the aggregated value for the interval key belongs to."""
    if not self._buckets:
      raise Exception("I don't know. Run Train() first.")

    position = bisect.bisect_left(self._buckets, (key, float("-inf")))
    if position >= len(self._buckets):
      position = len(self._buckets) - 1
    unused_key, value = self._buckets[position]
    return value
