from distutils.core import setup
from distutils.extension import Extension
from att.test import RunAll

setup(
  name="ATT",
  cmdclass={"test": RunAll},
  ext_modules=ext_modules,
  install_requires = [
    'lxml',
    'numpy',
    'pyyaml',
    'nltk',
    'cython',
    'pylint',
    'sphinx',
    'docutils',
    'jinja2',
    'pygments',
    'unittest']
)

