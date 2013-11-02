===============================
First n documents from a corpus
===============================

To restrict a corpus to first n documents, use the following configuration
in any place where a corpus is required:

.. code-block:: yaml
  :linenos:

  class: CorpusHead
  n: number_of_documents
  corpus:
    class: CorpusName
    corpus_setting_1: corpus_setting_value1
    ...

where ``number_of_documents`` is the number of documents you want to
be considered. The indented part should contain the description of the
corpus you want to restrict.
