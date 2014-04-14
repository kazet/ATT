======================
Rendering an alignment
======================

If you want to render an alignment, use ``render_alignment.py``.

First, run ``. venv/bin/activate`` to enter the Python virtual environment
(if you didn't already create it, refer to :doc:`/installation`).

Then, run ``render_alignment.py`` with the following options:

--input_folder
  The folder with TMX files, one per document (as returned by ``align.py``).
--output_folder
  The folder you want the HTML results to be written to.
--languages
  Space-separated list of languages you want to be extracted.
