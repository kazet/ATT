=========================
SentenceSimilarityAligner
=========================

To use the sentence similarity aligner, put the following in the aligner configuration
file:

.. code-block:: yaml
   :linenos:

   class: SentenceSimilarityAligner
   signals:
     - class: Signal1
       signal_setting_1: signal_setting_value1
       ...
     - class: Signal2
       signal_setting_1: signal_setting_value1
       ...
     ...

Signals are ways to measure sentence similarity based on some sentence
features. The "optimal" list of signals (but, for different corpora and
language pairs, YMMV) is:

* SizeRatioSignal
* CommonTokensSignal
* TokenStartSignal
* UniqueTokensSignal
* DictionaryWordsSignal

See :doc:`sentence_similarity_aligner_signals`.
