==================
Module conventions
==================

One class per file?
-------------------

If you decide to follow this convention in a new package, import them in
the ``__init__.py`` file so that only one ``from xyz import A, B, ...``
directive is needed.

Naming
------

Module names should follow the naming enforced by lint, i.e. match the
``[a-z][a-z0-9_]{2,30}`` regular expression.


Factories
---------

See :doc:`subclassing_conventions`

Docstrings
----------

Module docstring should link to any documentation related. Use document names
in the docstrings.
