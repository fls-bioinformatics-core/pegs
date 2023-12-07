Version History and Changes
===========================

--------------------------
Version 0.6.6 (2023-12-07)
--------------------------

* Fix continuous integration testing workflow in Github
  Actions to work with Python 3.6.
* Pin required version of ``xlsxwriter`` to 3.1.9, and
  fix associated bug when creating XLSX files with TADS
  using this version.
* Fix documentation generation on ReadTheDocs.
* Add ``CITATION.cff`` file to GitHub repository (adds
  citation information to the repository front page).

--------------------------
Version 0.6.5 (2022-07-01)
--------------------------

* Always use the ``Agg`` ``matplotlib`` backend (to
  avoid problems with systems where ``DISPLAY``
  environment variable is set but no graphical
  display is available.
* Update documentation for ``mk_pegs_intervals`` to
  clarify how to obtain suitable input files.

--------------------------
Version 0.6.4 (2021-11-08)
--------------------------

* Update the citation information following publication
  of supporting paper on F1000Research
  (https://f1000research.com/articles/10-570/v2)

--------------------------
Version 0.6.3 (2021-10-25)
--------------------------

* Patches to improve handling of input files: fix
  problems with sorting filenames, and perform explicit
  checks on peaks and cluster files to ensure that they
  exist and are not actually directories.
* Update the Conda installation instructions in the
  ``README`` and documentation.

--------------------------
Version 0.6.2 (2021-09-28)
--------------------------

* Update the ``README`` and "getting started"
  documentation to include installation from Conda.

--------------------------
Version 0.6.1 (2021-09-14)
--------------------------

* Patches to update the ``README`` and glucocorticoid
  examples to reflect the  new command line format
  introduced in version 0.6.0.

--------------------------
Version 0.6.0 (2021-09-14)
--------------------------

**This version includes updates that are not backwards
compatible with older versions of PEGS**

* Substantial update to how input files and distances
  are specified:
  - New compulsory ``--peaks`` and ``--genes``
    arguments must now be used to specify one or more
    peakset and gene cluster files respectively.
  - Distance intervals must be specified with new
    ``--distances`` option.
* New options added to customise the output heatmaps:
  - ``--x-label`` and ``--y-label`` options allow custom
    axis labels to be specified.
  - Documentation on setting custom colours for heatmap
    has been expanded (along with examples).
  - Heatmap image format can be specified on the command
    line either implicitly (via output file name extension)
    or explicitly (using ``--format`` option). Supports
    PNG, SVG, PDF etc.
* Added information on how to cite PEGS.

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
