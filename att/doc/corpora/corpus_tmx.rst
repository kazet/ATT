==========
TMX Corpus
==========

To use a corpus in TMX format, put the following in the corpus configuration
file:

.. code-block:: yaml
  :linenos:

  class: CorpusTMX
  languages:
    - lang1
    - lang2
    - ...
    data_location: files_location

Where ``lang_1``, ``lang2``, ... are the language identifiers (:doc:`/languages`),
the ``identifiers_file`` file should contain
document identifiers (file names, each document should reside in a separate
file) you want to be considered. File names will be prefixed by the
``data_location`` setting value (the full path will be the configuration
file path/``data_location``/identifier).

Using DGT translation memory
----------------------------
For example, if you want to use the DGT translation memory to train or
evaluate aligners, download any subset of the files listed in
http://open-data.europa.eu/en/data/dataset/dgt-translation-memory ,
unzip them and create the following configuration (assuming you want to
consider only English and Polish):

.. code-block:: yaml
  :linenos:

  class: CorpusTMX
  languages:
   - "en"
   - "pl"
  data_location: "unziped_dgt_memory_location/"

