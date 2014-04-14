============
Dictionaries
============

Some tools, e.g. the aligner, require a dictionary. You can use
any dictionary available (for common languages, :doc:`/dictionaries/cfs_dictionary`
is a good choice) or write a new one. If you have to align a corpus with texts
in languages that are not suported by any dictionary, use 
:doc:`/dictionaries/empty_dictionary`.

To use a dictionary, set ``--dictionary`` to the name of the dictionary configuration
file. The format of the configuration file differs between dictionary classes -
see the respective dictionary documentation.


Writing a new dictionary
------------------------
See: :doc:`/code/subclassing_conventions`.
