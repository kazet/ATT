=========
Languages
=========

Languages are referred to in the configuration files by their codes.


=====  =======
Code   Name   
=====  =======
en     English
de     German
es     Spanish
pl     Polish
=====  =======

To add a new language, put it in the ``Languages.LANGUAGES`` variable of the
``att/language/languages.py`` file. By default you have to configure the
following parameters:

 code
   The language code
 name 
   The language human-readable name
 id
   The language unique identifier (simply add 1 to the second one's identifier)

The following two parameters are automatically detected. If you want them
to be different than ``lowercase(name)``, you may want to set them by hand:

 nltk_name
   The language name used  by NTLK
 cfs_name
   The language name used by CFS (See: :doc:`/dictionaries/cfs_dictionary`)
