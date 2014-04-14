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
#. ``python setup.py install`` to install all required packages and ATT.

After that, ``train.py``, ``test_aligner.py``, ``align.py`` and ``render_alignment.py`` will
be available in your virtualenv.

You probably want to train an aligner (:doc:`training_aligners`) and then evaluate it
(:doc:`testing_aligners`) or use it to align a corpus (:doc:`aligning`).
