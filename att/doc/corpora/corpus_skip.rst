====================================
Skip first n documents from a corpus
====================================

To skip first n documents in a corpus (and use the rest for training or
evaluation), use the following configuration in any place where a corpus
is required:

.. code-block:: yaml
  :linenos:

  class: CorpusSkip
  n: number_of_documents
  corpus:
    class: CorpusName
    corpus_setting_1: corpus_setting_value1
    ...

where ``number_of_documents`` is the number of documents you want to
be skipped. The indented part should contain the description of the corpus
you want to restrict.
