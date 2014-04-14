================
Testing aligners
================

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``test_aligner.py`` with the following options:

--dictionary
  The configuration file of the dictionary that will be used by the aligner
  (see: :doc:`/dictionaries/index`).
--corpus
   The name of the corpus you want to use for evaluation. Remember to use
   different training and testing corpora to avoid overfitting.
--trained_aligner
   The name of the file that contains the trained aligner (written by
   ``train.py``).
--v
   Verbose level (use -v to see some information messages, -vv to see
   debug messages and -vvv to see everything - the last option is slow
   and should not be used if you're not debugging the program).

Example
-------

Suppose you trained a random aligner, saved it to ``trained_aligner`` and want
to test how good it is on the DGT translation memory.

First, download any subset of the files listed in
http://open-data.europa.eu/en/data/dataset/dgt-translation-memory ,
unzip them and configure the test corpus by putting the following in
``testing_corpus.yml``:

.. code-block:: yaml
  :linenos:

  class: CorpusHead
  n: 20 # currently alignment is slow, so it's not a good idea to align the
        # whole corpus - CorpusHead will return only the first 20 documents
  corpus: 
    class: CorpusTMX
    languages:
      - "en"
      - "pl"
      - "fr"
    data_location: "unziped_dgt_memory_location/"

Then, run:

``test_aligner.py --trained_aligner trained_aligner --corpus testing_corpus.yml -vv``
