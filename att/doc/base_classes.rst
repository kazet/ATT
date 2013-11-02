============
Base classes
============

Alignment
---------

Defined in att/alignment.py. Represents an alignment and consists of a document
and a list of matches, each match being a list of (language, sentence number,
starting from 0).

Document
--------

Defined in att/document.py. Represents a document in only one language.

Multilingual document
---------------------

Defined in att/multilingual_document.py. Consists of a list of Document objects
and represents a document translated into several languages.
