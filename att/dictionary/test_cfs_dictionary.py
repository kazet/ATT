# pylint: disable=R0904,R0921,C0111

import os
from att.dictionary.cfs_dictionary import CFSDictionary
from att.language import Languages
from att.test import TestCase

class LogTestCase(TestCase):
  def testTranslation(self):
    cfs_dictionary = CFSDictionary({
      'path': os.path.join(os.path.dirname(__file__), 'fixtures'),
      'languages': ['pl', 'de']})

    self.assertTrue(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'pewien',
        Languages.GetByCode('de'), 'ein'))

    self.assertTrue(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'pewien',
        Languages.GetByCode('de'), 'eIn'))

    self.assertFalse(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'pewien',
        Languages.GetByCode('de'), 'schmetterling'))

    # test English special case
    self.assertTrue(cfs_dictionary.IsTranslation(
        Languages.GetByCode('en'), 'abandonment',
        Languages.GetByCode('de'), 'verlassenheit'))

    # test prefix-based "stemming"
    self.assertTrue(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'porzucenia',
        Languages.GetByCode('de'), 'verlassenheiten'))

    # test ambigupus prefixes
    self.assertFalse(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'p',
        Languages.GetByCode('de'), 'abkommen'))

    self.assertFalse(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'mlewnmfpopwefpojwwfopwej',
        Languages.GetByCode('de'), 'ein'))

    self.assertFalse(cfs_dictionary.IsTranslation(
        Languages.GetByCode('pl'), 'pewien',
        Languages.GetByCode('de'), 'mlewnmfpopwefpojwwfopwej'))
