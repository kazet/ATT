================
Testing aligners
================

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``test_aligner.py`` with the following options:

corpus
   The name of the corpus you want to use for evaluation. Remember to use
   different training and testing corpora to avoid overfitting.
trained_aligner
   The name of the file that contains the trained aligner (written by
   ``train.py``).
v
   Verbose level (use -v to see some information messages, -vv to see
   debug messages and -vvv to see everything - the last option is slow
   and should not be used if you're not debugging the program).
