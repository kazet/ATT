att
===
This is a tool to train and test various multilingual (i.e.
with more than two languages) parallel text alignment algorithms.

It was a part of my 2015 M.S. thesis, *Multilingual corpus
alignment algorithms*, and is not maintained anymore.

For more information, please contact
[krzysztof.zajac2@gmail.com](mailto:krzysztof.zajac2@gmail.com).

Building documentation
----------------------

To build the documentation, run the following:

* Install the following packages: `python-virtualenv`, `libxml2-dev`,
  `libxslt-dev`, `python-pip` and `python-dev`.

And execute the following commands:

```bash
cd att/
virtualenv venv
. venv/bin/activate
python setup.py install
cd att/doc/
make html
```

The documentation table of contents will be written to
`att/doc/_build/index.html`

Training aligners
-----------------

Suggested aligner to use is CombinedDynamicSentenceSimilarityAligner.
To train it, build the documentation and follow the instructions in
`att/doc/_build/training_aligners.html`

Testing aligners
----------------

To test an aligner, build the documentation and follow the instructions in
`att/doc/_build/testing_aligners.html`
