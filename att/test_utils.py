import math

from att.test import TestCase
from att.utils import \
  GroupByKey, \
  Average, \
  SetSimilarity, \
  ListSimilarity, \
  EnumeratePairs, \
  Gauss, \
  LongestCommonSubstring, \
  Flatten

class UtilsTestCase(TestCase):
  def test_longest_common_substring(self):
    self.assertEqual(LongestCommonSubstring("", ""), "")
    self.assertEqual(LongestCommonSubstring("b", "a"), "")
    self.assertEqual(LongestCommonSubstring("abbaca", "abbaca"), "abbaca")
    self.assertEqual(LongestCommonSubstring("politechnika", "toaleta"), "olta")

  def test_list_similarity(self):
    self.assertAlmostEqual(ListSimilarity([1, 2], [2, 1]), 2.0 / 4.0)
    self.assertAlmostEqual(ListSimilarity([2, 2], [2, 2]), 2.0 / 4.0)
    self.assertAlmostEqual(ListSimilarity([1, 2], [3, 4]), 0.0)
    self.assertAlmostEqual(ListSimilarity([], []), 0.0)

  def test_sett_similarity(self):
    self.assertAlmostEqual(SetSimilarity(set([1, 2]), set([2, 1])),
                           2.0 / 4.0)
    self.assertAlmostEqual(SetSimilarity(set([2, 2]), set([2, 2])),
                           2.0 / 4.0)
    self.assertAlmostEqual(SetSimilarity(set([1, 2]), set([3, 4])),
                           0.0)
    self.assertAlmostEqual(SetSimilarity(set([]), set([])), 0.0)

  def test_gauss(self):
    value = Gauss(
      1,
      center=1,
      standard_deviation=1.0/math.sqrt(math.pi * 2))
    self.assertEquals(value, 1)

  def test_group_by_key(self):
    groups = GroupByKey([(1, 1), (0, 0), (1, 1), (2, 2)])
    self.assertUnorderedEqual(groups, [
      [(0, 0)],
      [(1, 1), (1, 1)],
      [(2, 2)]])

    groups = GroupByKey([(1, 1), (1, 1), (1, 1), (1, 1)])
    self.assertUnorderedEqual(groups, [
      [(1, 1), (1, 1), (1, 1), (1, 1)]])

    groups = GroupByKey([])
    self.assertUnorderedEqual(groups, [])

    groups = GroupByKey([(1, 1), (2, 2), (2, 2)])
    self.assertUnorderedEqual(groups, [
      [(1, 1)],
      [(2, 2), (2, 2)]])

    groups = GroupByKey([(1, 1), (2, 2), (3, 3)])
    self.assertUnorderedEqual(groups, [
      [(1, 1)],
      [(2, 2)],
      [(3, 3)]])

  def test_enumerate_pairs(self):
    self.assertUnorderedEqual(EnumeratePairs([]), [])
    self.assertUnorderedEqual(EnumeratePairs([1]), [])
    self.assertUnorderedEqual(
      EnumeratePairs([1, 2, 3]),
      [(1, 2), (1, 3), (2, 3)])

  def test_flatten(self):
    self.assertAlmostEqual(Flatten([]), [])
    self.assertAlmostEqual(Flatten([[1]]), [1])
    self.assertAlmostEqual(Flatten([[1, 2], [3, 4]]), [1, 2, 3, 4])
    self.assertAlmostEqual(Flatten([[], [1], []]), [1])

  def test_average(self):
    self.assertAlmostEqual(Average([1, 2]), 1.5)
    self.assertAlmostEqual(Average([1, 1]), 1)
    self.assertAlmostEqual(Average([1]), 1)
    self.assertRaises(ZeroDivisionError, Average, [])
