==================
Viewing alignments
==================

If you want to view an alignment, use ``render_alignment.py``.

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``render_alignment.py`` with the following options:

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
