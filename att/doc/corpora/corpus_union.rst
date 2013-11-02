=========================
Sum two (or more) corpora
=========================

To use more corpora for training or alignment, use the following configuration
in any place where a corpus is required:

.. code-block:: yaml
  :linenos:

  class: CorpusUnion
  corpora:
  - class: CorpusName1
    corpus_setting_1: corpus_setting_value1
    ...
  - class: CorpusName2
    corpus_setting_1: corpus_setting_value1
    ...

Each indented part (starting with a dash) should contain a description of a
corpus.
