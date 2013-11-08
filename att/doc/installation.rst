================
ATT installation
================

#. ``cd align``
#. Install the following packages: ``python-virtualenv``, ``libxml2-dev``,
   ``libxslt-dev``, ``python-pip`` and ``python-dev`` (Use Google if you use
   different Linux distribution than Debian and want to figure out the correct
   package names).
#. ``virtualenv venv`` to create a virtual Python environment where installed
   packages will be stored (so that you can update them independelntly from the
   global ``site-packages`` directory).
#. ``pip install -r requirements`` to install all the packages listed in the
   ``requirements`` file in the virtual environment.
#. ``python setup.py build_ext --inplace`` to  compile the C part of the aligner.
   Later, this command will install the whole ATT package, as soon as I code it.
#. ``python -m nltk.downloader -d venv/nltk_data all`` to install NLTK data,
   models (such as sentence tokenization models for various languages) and
   corpora.

