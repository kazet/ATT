========================================
CombinedDynamicSentenceSimilarityAligner
========================================

How it works
------------

This aligner combines bilingual alignments into multilingual alignments.

Usage
-----

To use this aligner, put the following in the aligner configuration file:

.. code-block:: yaml
   :linenos:

   class: CombinedDynamicSentenceSimilarityAligner
   languages:
     - language_code_1
     - language_code_2
     - ...
   signals:
     - class: Signal1
       signal_setting_1: signal_setting_value1
       ...
     - class: Signal2
       signal_setting_1: signal_setting_value1
       ...
     ...


Suggested configuration:

.. code-block:: yaml
   :linenos:

   class: CombinedDynamicSentenceSimilarityAligner
   languages:
     - "en"
     - "de"
     - "es"
     - "pt"
     - "fr"
     - "hu"
     - "el"
     - "sv"
     - "pl"
   signals:
     - class: SizeRatioSignal
     - class: CommonTokensSignal
     - class: TokenStartSignal
     - class: UniqueTokensSignal
     - class: DictionaryWordsSignal

For signal documentation, see :doc:`/aligners/sentence_similarity_aligner`.
