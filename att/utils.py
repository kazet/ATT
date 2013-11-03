import math

def First(tup):
  """Return the first element of a tuple or a list. Just for verboseness
  of code that uses it."""
  return tup[0]

def Second(tup):
  """Return the second element of a tuple or a list. Just for verboseness
  of code that uses it."""
  return tup[1]

def GroupByKey(data):
  """Groups the list by its keys. This function will return a list of buckets,
  each of them containing all list elements with the same key."""
  data.sort(key=lambda (key, unused_value): key)
  buckets = []
  last = None
  bucket = []
  for key, value in data:
    if last is not None and last != key and bucket:
      buckets.append(bucket)
      bucket = []
    last = key
    bucket.append( (key, value) )
  if bucket:
    buckets.append(bucket)
  return buckets


def Average(lst):
  """Return the list average."""
  return sum(lst) / float(len(lst))


def Gauss(x, standard_deviation=1, center=0):
  """Calculate the normal distribution."""
  return \
    math.exp((-(x - center) ** 2) / 2 * standard_deviation * 2) / \
    (standard_deviation * math.sqrt(2.0 * math.pi))


def SetSimilarity(s1, s2):
  """Returns the size of the largest common subset of s1 and s2
  divided by their length combined or 0 if both are empty."""
  if not s1 and not s2:
    return 0
  return len(s1 & s2) / float(len(s1) + len(s2))

def NumCommonElements(s1, s2):
  """Return the number of common elements in s1 and s2."""
  if not s1 and not s2:
    return 0
  s1_sorted = sorted(s1)
  s2_sorted = sorted(s2)
  s1_iter = 0
  s2_iter = 0
  num_common = 0
  while s1_iter < len(s1_sorted) and s2_iter < len(s2_sorted):
    if s1_sorted[s1_iter] < s2_sorted[s2_iter]:
      s1_iter += 1
    elif s1_sorted[s1_iter] > s2_sorted[s2_iter]:
      s2_iter += 1
    else:  # equal
      num_common += 1
      s1_iter += 1
      s2_iter += 1
  return num_common

def ListSimilarity(s1, s2):
  """Returns the size of the largest common subset of s1 and s2
  elements divided by their length combined or 0 if both are empty."""
  if not s1 and not s2:
    return 0
  return NumCommonElements(s1, s2) / (1.0 * (len(s1) + len(s2)))

def HaveCommonElement(s1, s2):
  """Returns True if s1 and s2 have at least one element in common,
  False otherwise."""
  return NumCommonElements(s1, s2) > 0

def EnumeratePairs(lst):
  """Enumerates all pairs in lst, without repeats ((A, B) and (B, A)
  are considered the same) and (A, A) pairs."""
  for first in range(0, len(lst)):
    for second in range(first + 1, len(lst)):
      yield (lst[first], lst[second])


def Flatten(lst):
  """Converts a list of lists into a list containing all elements
  from any element of the previous list."""
  lst_sum = []
  for item in lst:
    lst_sum.extend(item)
  return lst_sum
