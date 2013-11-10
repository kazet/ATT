=============================
GrowSentenceSimilarityAligner
=============================

How it works
------------

This aligner starts with an one-language match right after the last match (or
separated with 1, 2, ... sentences) and greedily adds sentences in different
languages to the math. The best one (because we have matches started from
different sentences in different languages) is then added to the alignment.

Usage
-----

To use the grow sentence similarity aligner, put the following in the aligner configuration
file:

.. code-block:: yaml
   :linenos:

   class: GrowSentenceSimilarityAligner
   signals:
     - class: Signal1
       signal_setting_1: signal_setting_value1
       ...
     - class: Signal2
       signal_setting_1: signal_setting_value1
       ...
     ...


For signal documentation, see :doc:`/aligners/sentence_similarity_aligner`.
