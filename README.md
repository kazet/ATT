att
===

Building documentation
----------------------

To build the documentation, run the following:

* Install python-virtualenv and python-pip packages

And execute the following commands:
* cd att/
* virtualenv venv
* python setup.py install
* cd att/doc/
* make html

The documentation table of contents will be written to
`att/doc/_build/index.html`

Training aligners
-----------------

Suggested aligner to use is CombinedDynamicSentenceSimilarityAligner.
To train it, follow the instructions in
`att/doc/_build/training_aligners.html`
