================
Aligning corpora
================

If you want to align a document, use ``align.py``.

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``align.py`` with the following options:

--dictionary
  The configuration file of the dictionary that will be used by the aligner
  (see: :doc:`/dictionaries/index`).
--corpus
   The name of the corpus you want to use for evaluation. Remember to use
   different training and testing corpora to avoid overfitting.
--render_reference
   Use this flag to write a file containing the reference alignment (one
   should be attached to the corpus you are aligning) next to the alignment
   file.
--trained_aligner
   The name of the file that contains the trained aligner (written by
   ``train.py``).
--output_folder
   The location of the output. Each document will be aligned and written
   to ``output_folder``/``doc_`` + document identifier + ``.html``
--v
   Verbose level (use -v to see some information messages, -vv to see
   debug messages and -vvv to see everything - the last option is slow
   and should not be used if you're not debugging the program).
