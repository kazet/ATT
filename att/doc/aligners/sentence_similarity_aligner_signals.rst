============================================
SentenceSimilarityAligner: available signals
============================================

Currently, the following signals are available:

PunctuationSignal
-----------------
The number of common punctuation characters thath both sentences have in
common.

This signal has one setting: ``characters``, a list of characters treated
as punctuation marks.

CommonTokensSignal
------------------
The number of common tokens (currently: words, numbers, etc.: anything existing
on the list returned by ``nltk.tokenize()``) (existing in both sentences)
divided by the length of both sentences.

This signal doesn't have any settings.

TokenStartSignal
----------------
The number of word prefixes of fixed length, existing in both sentences divided
by the length of both sentences. To set the prefix length, set the ``length``
configuration option.

WordCountRatioSignal
--------------------
The logarithm of the number of words in the first sentence divided by the
number of words in the second one.

This signal doesn't have any settings.


SizeRatioSignal
---------------

The logarithm of (the number of characters in the first sentence divided by
the number of characters in the second one).

This signal doesn't have any settings.

DictionaryWordsSignal
---------------------
The number of words existing in both sentences.
If one of the sentences is not in English, each word will be translated
using a dictionary (and if it doesn't exist in the dictionary, and there
exist a prefix of the word such that there is only one word starting with
this prefix in the dictionary, the word from the dictionary will be used).

To use the signal, configure the dictionary (see :doc:`/dictionaries/index`).
For example, for the CFS dictionary, use the following aligner configuration:

.. code-block:: yaml
   :linenos:

   class: SentenceSimilarityAligner
   signals:
     - class: ...
     - class: ...
     - class: ...
     - class: DictionaryWordsSignal
       dictionary:
         class: CFSDictionary
         path: unzipped_dictionary_path
         languages:
           - "en"
           - "de"
           - ...
           - ...
           - ...
