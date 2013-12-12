import sys

from att import global_context


class VerboseLevel(object):
  ERROR = 0
  INFO = 1
  DEBUG = 2
  DEBUG_FULL = 3


def LogDebugFull(*args):
  """If log level is at least VerboseLevel.DEBUG_FULL,
  Prints the first argument with all following passed as the
  format arguments to the first one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.DEBUG_FULL:
    Log(*args)


def LogDebug(*args):
  """If log level is at least VerboseLevel.DEBUG,
  Prints the first argument with all following passed as the
  format arguments to the first one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.DEBUG:
    Log(*args)

def LogInfo(*args):
  """If log level is at least VerboseLevel.INFO,
  Prints the first argument with all following passed as the
  format arguments to the first one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.INFO:
    Log(*args)

def LogInfoClear(*args):
  """If log level is at least VerboseLevel.INFO,
  Prints the first argument with all following passed as the
  format arguments to the first one so that the current line gets
  cleared and replaced with the new one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.INFO:
    LogClear(*args)

def LogError(*args):
  """If log level is at least VerboseLevel.ERROR,
  Prints the first argument with all following passed as the
  format arguments to the first one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.ERROR:
    Log(*args)

def FormatForLogs(*args):
  if len(args) > 1:
    return unicode(args[0] % tuple(args[1:]))
  else:
    return unicode(args[0])

def Log(*args):
  """Prints the first argument with all following passed as the
  format arguments to the first one."""
  sys.stderr.write("%s\n" % FormatForLogs(*args))

def LogClear(*args):
  """Prints the first argument with all following passed as the
  format arguments to the first one so that the current line gets
  cleared and replaced with the new one."""
  sys.stderr.write("\r\x1B[2K%s" % FormatForLogs(*args))

