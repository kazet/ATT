# pylint: disable=R0904,R0921,C0111

from att.test.test_case import TestCase
from att.test.mock_writable_file import MockWritableFile

class MockWritableFileTestCase(TestCase):
  def testBasicBehavior(self):
    mock_writable_file = MockWritableFile()
    mock_writable_file.write('a')
    mock_writable_file.write('b')

    mock_writable_file.ClearContents()
    mock_writable_file.write('c')
    mock_writable_file.write('d')

    self.assertEqual(mock_writable_file.GetContents(), 'cd')
