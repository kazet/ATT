from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

default_extra_compile_args=["-O3", "-Wall"]
default_libraries=["m"]

class DefaultExtension(Extension):
  def __init__(self,
               module,
               additional_sources=[],
               extra_compile_args=default_extra_compile_args,
               libraries=default_libraries):
    source = '%s.pyx' % module.replace('.', '/')
    Extension.__init__(
      self,
      module,
      [source] + additional_sources,
      extra_compile_args=extra_compile_args,
      libraries=libraries)

ext_modules=[
    DefaultExtension("att.classifier.signal_aggregator"),
    DefaultExtension("att.classifier.fast_bucket_average"),
]



setup(
  name = "ATT",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)
