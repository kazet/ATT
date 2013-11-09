import math

from att.test import TestCase
from att.utils import \
  GroupByKey, \
  Average, \
  SetSimilarity, \
  ListSimilarity, \
  DictUpdateWithString, \
  EnumeratePairs, \
  Gauss, \
  LongestCommonSubstring, \
  TupleSplit, \
  Flatten

class UtilsTestCase(TestCase):
  def test_dict_update_with_string(self):
    updated = DictUpdateWithString({'a': {'b': 2, 'c': 3}, 'd': 4},
        'a.b=int:4;d=int:5')
    self.assertEqual(updated, {'a': {'b': 4, 'c': 3}, 'd': 5})
    updated = DictUpdateWithString({'a': {'b': 2, 'c': 3}, 'd': 4}, 'd=int:5')
    self.assertEqual(updated, {'a': {'b': 2, 'c': 3}, 'd': 5})
    updated = DictUpdateWithString({'a': {'b': 2, 'c': 3}, 'd': 4}, '')
    self.assertEqual(updated, {'a': {'b': 2, 'c': 3}, 'd': 4})

    # test nonexistent formats
    self.assertRaises(
        ValueError,
        DictUpdateWithString,
        {'a': {'b': 2, 'c': 3}, 'd': 4},
        'd=xyzzy:4')

    # test empty positions
    self.assertRaises(
        KeyError,
        DictUpdateWithString,
        {'a': {'b': 2, 'c': 3}, 'd': 4},
        '=int:4')

    # test adding keys
    updated = DictUpdateWithString({'a': {'b': 2, 'c': 3}, 'd': 4}, 'e=int:6')
    self.assertEqual(updated, {'a': {'b': 2, 'c': 3}, 'd': 4, 'e': 6})

    # test adding subkeys
    updated = DictUpdateWithString({'a': {'b': 2, 'c': 3}, 'd': 4}, 'e.f=int:6')
    self.assertEqual(updated, {'a': {'b': 2, 'c': 3}, 'd': 4, 'e': {'f': 6} })

    # test if not dict copying happens
    adict = {'a': {'b': 2, 'c': 3}, 'd': 4}
    updated = DictUpdateWithString(adict, 'd=int:5')
    self.assertEqual(updated, {'a': {'b': 2, 'c': 3}, 'd': 5})
    self.assertEqual(adict, {'a': {'b': 2, 'c': 3}, 'd': 5})
    # see if they are both the same thing in memory
    updated['d'] = 6
    self.assertEqual(adict['d'], 6)

  def test_tuple_split(self):
    self.assertEqual(TupleSplit("a=b", "=", 2), ("a", "b") )
    self.assertEqual(TupleSplit("a.b", ".", 2), ("a", "b") )
    self.assertEqual(TupleSplit("a", ".", 1), ("a",) )
    self.assertRaises(ValueError, TupleSplit, "a", ".", 2)

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
