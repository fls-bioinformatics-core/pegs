Version History and Changes
===========================

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
