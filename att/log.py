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

def LogError(*args):
  """If log level is at least VerboseLevel.ERROR,
  Prints the first argument with all following passed as the
  format arguments to the first one."""
  if global_context.global_context.GetArgs().verbose >= VerboseLevel.ERROR:
    Log(*args)

qi = 0
def Log(*args):
  """Prints the first argument with all following passed as the
  format arguments to the first one."""
  global qi

  qi += 1

  if qi > 300:
    return

  if len(args) > 1:
    print >> sys.stderr, unicode(args[0] % tuple(args[1:]))
  else:
    print >> sys.stderr, unicode(args[0])
