Version History and Changes
===========================

--------------------------
Version 0.5.1 (2021-05-12)
--------------------------

* Patches to fix display of ``README`` landing page on
  PyPI and include the changelog in the documentation.

--------------------------
Version 0.5.0 (2021-05-12)
--------------------------

* Added support for Python 3.9.
* Dropped support for Python 2.7.
* Fixed bug with automatic installation of ``bedtools``
  (was failing on some systems).
* Updated versions of dependencies: ``numpy`` (1.19.5),
  ``scipy`` (1.5.4), ``matplotlib`` (3.3.4) and
  ``seaborn`` (0.11.1).
* Update to installation information to indicate that
  ``PEGS`` can be installed directly from PyPI.

--------------------------
Version 0.4.2 (2021-05-12)
--------------------------

* Updates to ``setup.py`` to enable distributions to be
  built for upload to the Python Package Index (PyPI).

--------------------------
Version 0.4.1 (2021-05-10)
--------------------------

* Fixes to the 'quick start' and 'licensing' sections of
  the ``README``
* Add worked example using mouse glucocorticoidal data to
  the ``README`` and the documentation.
* Update requirement for Pillow library to 8.1.1.
* Fix unit tests and add continuous integration testing
  workflow in Github Actions.

--------------------------
Version 0.4.0 (2020-08-18)
--------------------------

* Drop the requirement that cluster files must be named
  ``cluster_*.txt``; all files in the clusters directory
  will now be included in the analysis. The file names
  (without the file extension) will be used as x-axis
  labels in the plots.

--------------------------
Version 0.3.0 (2020-05-13)
--------------------------

* Automatically install a local version of ``bedtools`` if
  one is not found on the user's ``PATH``.

--------------------------
Version 0.2.0 (2020-03-20)
--------------------------

* Use ``bedtools intersect`` instead of ``intersectBed`` to
  calculate overlaps.
* Cosmetic updates to reporting program progress.
* Add initial Sphinx documentation.

--------------------------
Version 0.1.0 (2020-01-30)
--------------------------

* Initial version of PEGS.
