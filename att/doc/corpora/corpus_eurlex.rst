=============
EurLex corpus
=============

To use the Eurlex corpus (documents will be downloaded from the Internet),
put the following in the corpus configuration file:

.. code-block:: yaml
  :linenos:

  class: CorpusEurlex
  languages:
    - lang1
    - lang2
    - ...
    identifiers_file: identifiers_file

Where ``lang_1``, ``lang2``, ... are the language identifiers (see
:doc:`/languages/`) and the ``identifiers_file`` file should contain
document identifiers you want to be considered.
