=========================
SentenceSimilarityAligner
=========================

``SentenceSimilarityAligner`` is a base class for all aligners that measure
sentence similarity to align sentences. There are currently two such aligners,
:doc:`/aligners/grow_sentence_similarity_aligner` and
:doc:`/aligners/dynamic_sentence_similarity_aligner`.

Signals are ways to measure sentence similarity based on some sentence
features. The "optimal" list of signals (but, for different corpora and
language pairs, YMMV) is:

* SizeRatioSignal
* CommonTokensSignal
* TokenStartSignal
* UniqueTokensSignal
* DictionaryWordsSignal

See :doc:`sentence_similarity_aligner_signals`.
