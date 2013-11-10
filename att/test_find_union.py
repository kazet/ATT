from att.test import TestCase
from att.find_union import FindUnion

class FindUnionTestCase(TestCase):
  def test_union(self):
    find_union = FindUnion()
    find_union.AddIfNotExists(1)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(3)
    find_union.Union(1, 2)
    self.assertEqual(find_union.Find(1), find_union.Find(2))
    self.assertNotEqual(find_union.Find(1), find_union.Find(3))
    self.assertNotEqual(find_union.Find(2), find_union.Find(3))

  def test_adding_existing_items(self):
    find_union = FindUnion()
    find_union.AddIfNotExists(1)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(3)
    find_union.Union(1, 2)
    find_union.AddIfNotExists(1)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(3)
    self.assertEqual(find_union.Find(1), find_union.Find(2))
    self.assertNotEqual(find_union.Find(1), find_union.Find(3))
    self.assertNotEqual(find_union.Find(2), find_union.Find(3))

  def test_multiple_unions(self):
    find_union = FindUnion()
    find_union.AddIfNotExists(1)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(3)
    find_union.AddIfNotExists(4)
    find_union.AddIfNotExists(5)
    find_union.Union(1, 2)
    find_union.Union(2, 3)
    find_union.Union(3, 4)
    find_union.Union(4, 5)
    self.assertEqual(find_union.Find(1), find_union.Find(5))
    self.assertEqual(find_union.Find(1), find_union.Find(4))
    self.assertEqual(find_union.Find(1), find_union.Find(3))
    self.assertEqual(find_union.Find(5), find_union.Find(2))
    self.assertEqual(find_union.Find(2), find_union.Find(4))

  def test_iter(self):
    find_union = FindUnion()
    find_union.AddIfNotExists(1)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(3)
    find_union.AddIfNotExists(2)
    find_union.AddIfNotExists(1)
    items = []
    for item in find_union:
      items.append(item)

    self.assertUnorderedEqual(items, [1, 2, 3])
