from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules=[
    Extension("c_signal_aggregator",
              ["att/c_att/signal_aggregator/signal_aggregator.pyx"],
              libraries=["m"]) # Unix-like specific
]

setup(
  name = "C_att",
  cmdclass = {"build_ext": build_ext},
  ext_modules = ext_modules
)

