from datetime import timedelta

from att.test import TestCase
from att.datetime_utils import \
  TimedeltaInSeconds, \
  SecondsToHuman

class UtilsTestCase(TestCase):
  def test_seconds_to_human(self):
    self.assertEqual(SecondsToHuman(0), "0 s")
    self.assertEqual(SecondsToHuman(61), "1 min 1 s")
    self.assertEqual(SecondsToHuman(3661), "1 h 1 min 1 s")
    self.assertEqual(SecondsToHuman(86460), "1 day 1 min")
    self.assertEqual(SecondsToHuman(86400 * 4), "4 days")

  def test_timedelta_in_seconds(self):
    d = timedelta(hours=3)
    self.assertEqual(TimedeltaInSeconds(d), 3 * 3600)
    d = timedelta(minutes=3)
    self.assertEqual(TimedeltaInSeconds(d), 3 * 60)
    d = timedelta(days=3)
    self.assertEqual(TimedeltaInSeconds(d), 3 * 86400)
    d = timedelta(days=1, hours=1, minutes=1, seconds=1)
    self.assertEqual(TimedeltaInSeconds(d), 86400 + 3600 + 60 + 1)
