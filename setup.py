from setuptools import setup

setup(
  name="ATT",
  package_data = {
    'att/html': [
        'dependencies/*',
        'templates/*'],
    'att/dictionary': [
        'cfs_dictionary.pyx',
        'fixtures/*'],
    'att': [
        'tokenize.pyx',
        'utils.pyx',
        'fixtures/test_utils/test_recursive_listing/file*',
        'fixtures/test_utils/test_recursive_listing/dir1/file*',
        'fixtures/test_utils/test_recursive_listing/dir1/dir2/file*'],
    'att/classifier': [
        'fast_bucket_average.pyx',
        'signal_aggregator.pyx'],
  },
  packages = [
    'att',
    'att/test',
    'att/corpus',
    'att/aligner',
    'att/html',
    'att/aligner/sentence_similarity_signals',
    'att/dictionary',
    'att/language',
    'att/classifier'],
  install_requires = [
    'lxml',
    'pyyaml',
    'nltk',
    'cython',
    'pylint',
    'sphinx',
    'docutils',
    'jinja2',
    'pygments',
    'unittest2'],
  scripts = [
    'train.py',
    'test_aligner.py',
    'render_alignment.py']
)

