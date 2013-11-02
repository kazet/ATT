==============
CFS Dictionary
==============

To use the CFS Dictionary, download it (from
http://cs.jhu.edu/~ccb/data/dictionaries/) and unpack into any directory.
Then put the following configuration in any place where a dictionary
is required:

.. code-block:: yaml
  :linenos:

  class: CFSDictionary
  path: 'CFS-dicts'
  languages:
    - "en"
    - "de"
    - "es"
    - "pl"

If you want to use any other languages, see :doc:`/languages` section.
