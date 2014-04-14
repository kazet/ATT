=================
Training aligners
=================

Aligners have a model of the language behavior you may want to train
(or load an existing one, but currently none are supplied). Trained aligners
have a different format, packing both the aligner configuration and the models,
so that it is harder to make a mistake and e.g. use aligner1 with aligner2's
model.

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``train.py`` with the following options:

--dictionary
  The configuration file of the dictionary that will be used by the aligner
  (see: :doc:`/dictionaries/index`).
--training_corpus
   The name of the corpus you want to use for training. Remember to use
   different training and testing corpora to avoid overfitting.
--output
   The name of the file training aligner will be written to.
--aligner
   The aligner you want to train. Currently no safety checks are performed
   to check, if the tested aligner matches the model you provide him, so be
   careful: it will fail silently or just produce weird results.
--training_set_size
  The number of documents that will be taken from the corpus to train the
  aligner. For more (>5) languages, 100 is enough.
--dictionary
  The dictionary (:doc:`/dictionaries/index`) that will be used for training.
  Currently it is required by all aligners. You can provide an empty
  dictionary, but currently none are available.
--v
   Verbose level (use -v to see some information messages, -vv to see
   debug messages and -vvv to see everything - the last option is slow
   and should not be used if you're not debugging the program).

Example
-------

Suppose you want to train the best aligner we have,
``/aligners/CombinedDynamicSentenceSimilarityAligner``
(:doc:`/aligners/combined_dynamic_sentence_similarity_aligner`) on the DGT TM
corpus to align English, French and Polish.

Step 0: follow :doc:`/installation`.

First, download any subset of the files listed in
http://open-data.europa.eu/en/data/dataset/dgt-translation-memory ,
unzip them and configure the corpus by putting the following in
``aligner.yml``:

.. code-block:: yaml
  :linenos:

  class: CorpusHead
  n: 200
  corpus:
    class: CorpusTMX
    languages:
      - "en"
      - "pl"
      - "fr"
    data_location: "unzipped_dgt_memory_location/"

Then, configure the aligner, by creating ``aligner.yml``:

.. code-block:: yaml
  :linenos:

  class: CombinedDynamicSentenceSimilarityAligner
  languages:
  - "en"
  - "fr"
  - "pl"
  signals:
   - class: SizeRatioSignal
   - class: CommonTokensSignal
   - class: TokenStartSignal
   - class: UniqueTokensSignal
   - class: DictionaryWordsSignal

Then, configure the dictionary. First, download the suggested dictionary
(http://cs.jhu.edu/~ccb/data/dictionaries/CFS.Dictionaries.tar.gz)
and extract it into the CFS-dictionaries directory. Then put the following
in the ``dictionary.yml`` configuration file:

.. code-block:: yaml
   :linenos:

   class: CFSDictionary
   path: 'CFS-dictionaries/dict'
   languages:
     - "en"
     - "fr"
     - "pl"

Then, run:

``python train.py --training_corpus corpus.yml --output trained_aligner --aligner aligner.yml --dictionary dictionary.yml -vvv``
