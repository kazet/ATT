============
Dictionaries
============

Some tools, i.e. the dictionary signal for
:doc:`/aligners/sentence_similarity_aligner`, require a dictionary. You can use
any dictionary available (for common languages, :doc:`/dictionaries/cfs_dictionary`
is a good choice) or write a new one. If you have to align a corpus with texts
in languages that are not suported by any dictionary, use 
:doc:`/dictionaries/empty_dictionary`.

Writing a new dictionary
------------------------
See: :doc:`/code/subclassing_conventions`.
