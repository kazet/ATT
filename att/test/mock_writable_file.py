"""See: `Testing' in the documentation."""

class MockWritableFile(object):
  """A mock pretending to be a writable file."""
  def __init__(self):
    self._contents = ''

  def write(self, string): # pylint: disable=C0103
    """Write a string to the file."""
    self._contents += string

  def ClearContents(self):
    """Reset the internal content buffer and pretend nothing has been written
    so far."""
    self._contents = ''

  def GetContents(self):
    """Return everything that has been written so far."""
    return self._contents
