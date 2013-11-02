import sys


class MockArgs(object):
  """Mock arguments (instead of argparse result) for GlobalContext.

  You may retrieve any keyword argument passed to __init__() later
  by writing objname.argname.
  """
  def __init__(self, **kwargs):
    self._kwargs = kwargs

  def __getattr__(self, arg):
    return self._kwargs[arg]


class GlobalContext(object):
  """Global context for the aligners, corpora etc. 

  Determines common program behaviour, such as global arguments.
  """

  def __init__(self):
    self._args = MockArgs(verbose=0)

  def SetArgs(self, args):
    self._args = args

  def GetArgs(self):
    return self._args


global_context = GlobalContext()
