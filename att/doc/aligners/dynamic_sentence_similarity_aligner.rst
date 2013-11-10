================================
DynamicSentenceSimilarityAligner
================================

How it works
------------

This aligner aligns only multilingual documents in two languages, using
dynamic programming to calculate the best alignment.

First, it starts with an alignment of two empty documents: 0 sentences in the
first language and 0 in the second one.

Then, for each sentence ID pair, (idA, idB), we can:

* Skip the first one (and use the alignment of the first idA - 1 sentences in
  the  first language and the first idB sentences in the second one).
* Skip the second one (and use the alignment of the first idA sentences in
  the  first language and the first idB - 1 sentences in the second one).
* Match these two sentences and add them to the best alignment of the first
  idA - 1 sentences in the first language and the first idB - 1 sentences in
  the second one.

Usage
-----

To use the dynamic programming sentence similarity aligner, put the following
in the aligner configuration file:

.. code-block:: yaml
   :linenos:

   class: DynamicSentenceSimilarityAligner
   signals:
     - class: Signal1
       signal_setting_1: signal_setting_value1
       ...
     - class: Signal2
       signal_setting_1: signal_setting_value1
       ...
     ...


For signal documentation, see :doc:`/aligners/sentence_similarity_aligner`.
