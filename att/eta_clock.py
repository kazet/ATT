import datetime
from att.datetime_utils import SecondsToHuman, TimedeltaInSeconds
from att.log import LogDebug

class ETAClock(object):
  def __init__(self, min_value, max_value):
    self._value = min_value
    self._min_value = min_value
    self._max_value = max_value
    self._start = datetime.datetime.now()
    self._last = datetime.datetime.now()

  def Tick(self, increment):
    self._value += increment
    now = datetime.datetime.now()
    if (now - self._last) > datetime.timedelta(seconds=1):
      self._last = datetime.datetime.now()
      elapsed = TimedeltaInSeconds(now - self._start)
      per_second = (self._value - self._min_value) / elapsed
      remaining = (self._max_value - self._value) / per_second
      LogDebug("%.1f%% %s elapsed, %.2f per second, %s remaining",
               100.0 * (self._value - self._min_value) /
                    (self._max_value - self._min_value),
               SecondsToHuman(elapsed),
               per_second,
               SecondsToHuman(remaining))