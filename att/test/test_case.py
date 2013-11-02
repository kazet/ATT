# pylint: disable=R0904
"""See: `Testing' in the documentation."""

import unittest
import copy

class TestCase(unittest.TestCase):
  """A better version of TestCase, supporting some kinds of assertions
  needed by ATT."""
  def assertUnorderedEqual(self, list_a, list_b): # pylint: disable=C0103
    """Assert that list_a and list_b contain the same elements."""
    a_prim = copy.copy(list(list_a))
    b_prim = copy.copy(list(list_b))
    self.assertEqual(sorted(a_prim), sorted(b_prim))

  def assertContains(self, haystack, needle): # pylint: disable=C0103
    """Assert that needle is an element of haystack."""
    self.assertTrue(needle in haystack)
