from unittest import TestLoader, TestResult
from distutils.core import Command
import os

class RunAll(Command):
  description = "run all tests"
  user_options = []

  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    loader = TestLoader()
    path = os.path.join(os.path.dirname(__file__), '../../')
    tests = loader.discover(path, pattern='test_*.py')
    result = TestResult()
    tests.run(result)
    print 'Test cases: %d' % tests.countTestCases()
    print 'Errors: %s' % len(result.errors)
    print 'Failures: %s' % len(result.failures)
    print 'Skipped: %s' % len(result.skipped)
    for test_case, traceback in result.errors + result.failures:
      print ''
      print '------------------------------ %s' % test_case
      print traceback
