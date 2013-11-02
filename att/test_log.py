import sys

from att import log
from att.global_context import global_context, MockArgs
from att.test import TestCase
from att.test import MockWritableFile

class LogTestCase(TestCase):
  def setUp(self):
    self._old_stderr = sys.stderr
    sys.stderr = MockWritableFile()

  def tearDown(self):
    sys.stderr = self._old_stderr

  def test_log_levels(self):
    global_context.SetArgs(MockArgs(verbose=0))
    log.LogDebug("1d")
    log.LogInfo("1i")
    log.LogError("1e")

    global_context.SetArgs(MockArgs(verbose=1))
    log.LogDebug("2d")
    log.LogInfo("2i")
    log.LogError("2e")

    global_context.SetArgs(MockArgs(verbose=2))
    log.LogDebug("3d")
    log.LogInfo("3i")
    log.LogError("3e")

    self.assertEqual(sys.stderr.GetContents(), "1e\n2i\n2e\n3d\n3i\n3e\n")

  def test_log_formatting(self):
    log.LogError("test1")
    self.assertEqual(sys.stderr.GetContents(), "test1\n")

    sys.stderr.ClearContents()
    log.LogError("test1 %s", "a")
    self.assertEqual(sys.stderr.GetContents(), "test1 a\n")
