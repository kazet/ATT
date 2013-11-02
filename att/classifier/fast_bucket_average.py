class FastBucketAverage(object):
  """Divide an interval into buckets and quickly calculate bucket average.

  Data added here should consist of key-value pairs, bucket number is
  calculated based on the keys."""
  def __init__(self, key_from, key_to, num_buckets):
    if key_to == key_from:
      raise Exception("keyspace length is 0")
    self._key_from = key_from
    self._key_to = key_to
    self._num_buckets = num_buckets
    self._sums = [0 for unused_i in range(0, num_buckets)]
    self._counts = [0 for unused_i in range(0, num_buckets)]
    self._global_sum = 0
    self._global_count = 0

  def __str__(self):
    buckets = ["[%.3f..%.3f: %.3f (%d)]" % (start, end, avg, count)
               for avg, start, end, unused_sum, count in self.GetBuckets()]
    return "[FastBucketAverage buckets: %s]" % ','.join(buckets)

  def GetBucketIdForKey(self, key):
    """Return the ID for the bucket appropriate for the key."""
    position = (key - self._key_from) / float(self._key_to - self._key_from)
    bucket = int(position * self._num_buckets)
    bucket = min(bucket, self._num_buckets - 1)
    bucket = max(bucket, 0)
    return bucket

  def GetGlobalAverage(self):
    """Return the average of all values added."""
    return self._global_sum / self._global_count

  def GetBucketForKey(self, key):
    """Return the data (sum of all values and the number of the values)
    of the bucket appropriate for the key."""
    bucket = self.GetBucketIdForKey(key)
    return (self._sums[bucket], self._counts[bucket])

  def MinBucketSize(self):
    """Return the size of the smallest bucket."""
    return min(self._counts)

  def Aggregate(self, key, value):
    """Add a (key, value) pair for the appropriate bucket for its key."""
    bucket = self.GetBucketIdForKey(key)
    self._sums[bucket] += value
    self._counts[bucket] += 1.0
    self._global_sum += value
    self._global_count += 1.0

  def GetBuckets(self):
    """Return a list, one tuple for each bucket.

    Bucket description tuple format: (
      value average (or 0 if no values),
      bucket beginning (in terms of key space),
      bucket end (in terms of key space),
      sum of all values in the bucket,
      number of all values in the bucket).
    """
    per_bucket = 1.0 * (self._key_to - self._key_from) / self._num_buckets
    return [(0 if self._counts[i] == 0 else self._sums[i] / self._counts[i],
             self._key_from + per_bucket * i,
             self._key_from + per_bucket * (i + 1),
             float(self._sums[i]),
             float(self._counts[i]))
            for i in range(0, self._num_buckets)]

  def SetBuckets(self, buckets):
    """Set the bucket content.

    The input format should be the same as for GetBuckets()."""
    self._global_sum = 0
    self._global_count = 0

    for i in range(0, self._num_buckets):
      self._sums[i] = buckets[i][3]
      self._counts[i] = buckets[i][4]
      self._global_sum +=  buckets[i][3]
      self._global_count += buckets[i][4]

  def Get(self, key):
    """Return the average of all values in the bucket appropriate
    for the key."""
    bucket = self.GetBucketIdForKey(key)
    if not self._counts[bucket]:
      return 0
    else:
      return self._sums[bucket] / self._counts[bucket]
