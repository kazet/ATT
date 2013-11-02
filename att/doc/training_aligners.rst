=================
Training aligners
=================

Aligners have a model of the language behavior you may want to train
(or load an existing one, but currently none are supplied). Trained aligners
have a different format, packing both the aligner configuration and the models,
so that it is harder to make a mistake and e.g. use aligner1 with aligner2's
model.

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``train.py`` with the following options:

training_corpus
   The name of the corpus you want to use for training. Remember to use
   different training and testing corpora to avoid overfitting.
output
   The name of the file training aligner will be written to.
aligner
   The aligner you want to train. Currently no safety checks are performed
   to check, if the tested aligner matches the model you provide him, so be
   careful: it will fail silently or just produce weird results.
v
   Verbose level (use -v to see some information messages, -vv to see
   debug messages and -vvv to see everything - the last option is slow
   and should not be used if you're not debugging the program).
