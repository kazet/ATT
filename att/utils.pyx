import math
import re
import os

def TupleSplit(string, separator, length):
  splitted = string.split(separator)
  if len(splitted) != length:
    raise ValueError("`%s' should consist of %d values separated with `%s'" % (
                     string,
                     length,
                     separator))
  else:
    return tuple(splitted)

def DictUpdateWithString(d, s):
  """Update a dictionary with a configuration string.
  Configuration string format:
  position1=value1;position2=value2;...;positionN=valueN,

  Position format: a dot-separated list of keys. key1.key2.key3
  will mean d[key1][key2][key3].

  Value format:
    unicode:value - a unicode string value
    float:value - a floating-point value"""
  def ParseValue(string):
    value_format, value = TupleSplit(string, ":", 2)
    if value_format == "unicode":
      return unicode(value)
    elif value_format == "float":
      return float(value)
    elif value_format == "int":
      return int(value)
    else:
      raise ValueError("Unknown format: %s" % value_format)

  if s == '':
    return d

  updates = s.split(";")
  for update in updates:
    key_path, value = TupleSplit(update, "=", 2)
    if key_path == '':
      raise KeyError("Empty position")
    keys = key_path.split(".")

    # find the dictionary to change
    subdict = d
    for key in keys[:-1]:
      if not key in subdict:
        subdict[key] = {}
      subdict = subdict[key]
    subdict[keys[-1]] = ParseValue(value)
  return d

def LongestCommonSubstring(a, b):
  """Returns the longest common substring of A and B."""
  a_utf8 = a.encode('utf-8')
  b_utf8 = b.encode('utf-8')
  cdef char* str1 = a_utf8
  cdef char* str2 = b_utf8
  cdef int len1 = len(a_utf8)
  cdef int len2 = len(b_utf8)
  cdef int i
  cdef int j
  cdef char x
  cdef char y
  result = ""
  lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
  for i in range(len1):
    for j in range(len2):
      x = str1[i]
      y = str2[j]
      if x == y:
        lengths[i+1][j+1] = lengths[i][j] + 1
      else:
        lengths[i+1][j+1] = \
            max(lengths[i+1][j], lengths[i][j+1])
  result = ""
  i = len1
  j = len2
  while i != 0 and j != 0:
    if lengths[i][j] == lengths[i-1][j]:
      i -= 1
    elif lengths[i][j] == lengths[i][j-1]:
      j -= 1
    else:
      assert str1[i-1] == str2[j-1]
      result = a[i-1] + result
      i -= 1
      j -= 1
  return result

def StripNonFilenameCharacters(name):
  """Strips (replaces with _) all characters that shouldn't exist in a
  filename."""
  return re.sub("[^a-zA-Z0-9.,_]", "_", name)

def MkdirIfNotExists(directory):
  """Creates a directory if it doesn't exists."""
  if not os.path.exists(directory):
    os.mkdir(directory)

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
  data.sort()
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
