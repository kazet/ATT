=======================
Subclassing conventions
=======================

To write a new subclass (for example a new dictionary, corpus or aligner), you
may want to follow the convention to help the code stay clean and make your
new shiny subclass available in any aligner or corpus configuration files).

#. Create a separate file, ``your_subclass.py``, in the ``att/folder/``
   directory (for aligners, folder will be ``aligners``, for dictionaries:
   ``dictionaries``, etc.) (optional: if you have a bunch of logically
   grouped, small classes, ignore this convention) and add
   ``from att.dictionaries.your_subclass import YourSubclass`` to
   ``att/folder/__init__.py``.

#. Define the class and register it in the factory to make it available in any
   configuration files, like here:

.. code-block:: python
   :linenos:

   from att.folder.base_class import BaseClass
   from att.folder.base_class_factory import BaseClassFactory

   @BaseClassFactory.Register
   class YourDictionary(BaseClass):

Now, if you use the class in any YAML configuration, like this:

.. code-block:: yaml
  :linenos:

  dictionary:
    class: YourNewShinyDictionary
    option1: value1
    option2: value2

All the options will be passed as the first constructor parameter for
``YourNewShinyDictionary``.
