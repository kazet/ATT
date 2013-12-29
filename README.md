att
===

Building documentation
----------------------

To build the documentation, run the following:

* Install the following packages: `python-virtualenv`, `libxml2-dev`,
  `libxslt-dev`, `python-pip` and `python-dev`.

And execute the following commands:
* cd att/
* virtualenv venv
* . venv/bin/activate
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

Testing aligners
----------------

To test an aligner, follow the instructions in
`att/doc/_build/testing_aligners.html`
