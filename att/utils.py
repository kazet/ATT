import math

def First(tup):
  return tup[0]

def Second(tup):
  return tup[1]

def GroupByKey(data):
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
  return sum(lst) / float(len(lst))


def Gauss(x, standard_deviation=1, center=0):
  return \
    math.exp((-(x - center) ** 2) / 2 * standard_deviation * 2) / \
    (standard_deviation * math.sqrt(2.0 * math.pi))


def SetSimilarity(s1, s2):
  """Returns the size of the largest common subset of s1 and s2
  divided by their length combined."""
  if not s1 and not s2:
    return 0
  return len(s1 & s2) / float(len(s1) + len(s2))

def NumCommonElements(s1, s2):
  if not s1 and not s2:
    return 0
  s1_s = sorted(s1)
  s2_s = sorted(s2)
  i = 0
  j = 0
  common = 0
  while i < len(s1_s) and j < len(s2_s):
    if s1_s[i] < s2_s[j]:
      i += 1
    elif s1_s[i] > s2_s[j]:
      j += 1
    else:  # equal
      common += 1
      i += 1
      j += 1
  return common

def ListSimilarity(s1, s2):
  """Returns the size of the largest common subset of s1 and s2
  elements divided by their length combined."""
  if not s1 and not s2:
    return 0
  return NumCommonElements(s1, s2) / (1.0 * (len(s1) + len(s2)))

def HaveCommonElement(s1, s2):
  return NumCommonElements(s1, s2) > 0

def EnumeratePairs(lst):
  for i in range(0, len(lst)):
    for j in range(i + 1, len(lst)):
      yield (lst[i], lst[j])


def Flatten(lst):
  lst_sum = []
  for item in lst:
    lst_sum.extend(item)
  return lst_sum
