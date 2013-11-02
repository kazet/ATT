def TimedeltaInSeconds(timedelta):
  return 86400 * timedelta.days + \
         timedelta.seconds + \
         0.000001 * timedelta.microseconds

def SecondsToHuman(seconds):
  seconds = int(seconds)
  result = ""
  if seconds >= 2 * 86400:
    result += " %s days" % (seconds / 86400)
    seconds = seconds % 86400
  if seconds >= 86400:
    result += " %s day" % (seconds / 86400)
    seconds = seconds % 86400
  if seconds >= 3600:
    result += " %s h" % (seconds / 3600)
    seconds = seconds % 3600
  if seconds >= 60:
    result += " %s min" % (seconds / 60)
    seconds = seconds % 60
  if seconds or result == "":
    result += " %s s" % seconds
  return result.strip()
