**************************
Running analyses with PEGS
**************************

Basic usage
===========

To run an analysis the basic command line is:

::

    pegs [options] GENE_INTERVALS --peaks PEAKSET [PEAKSET ...] --genes CLUSTER [CLUSTER ...]

where:

 * ``GENE_INTERVALS`` is a set of reference transcription
   start sites (TSSs) for all genes; it can either be the
   name of a built-in reference set (for example "mm10"),
   or file with BED interval data
 * ``PEAKSET`` is a BED file containing input ChIP-seq
   peaks data (or other genomic intervals)
 * ``CLUSTER`` is a file defing a gene cluster

``PEGS`` will then calculate the enrichments (p-values and
counts) using a default set of genomic distances around the
input intervals in each of the peak-sets.

By default the program outputs a PNG heatmap called
``pegs_heatmap.png``, and an XLSX file with the p-values and
count data called ``pegs_results.xlsx``.

The formats and naming conventions for the various files are
described in :doc:`inputs` and :doc:`outputs`.

.. warning::

   This is a change in version 0.6.0 to the previous way of
   specifying peaksets and gene cluster via directories, which
   is no longer supported but can replicated using a command
   line of the form:

   ::

       pegs [options] GENE_INTERVALS --peaks PEAKS_DIR/* --genes CLUSTERS_DIR/*


Specifying genomic distances (``-d``, ``--distances``)
======================================================

The default set of genomic distances used in the enrichment
calculations can be overriden with a custom set of intervals
specified using the ``-d`` or ``--distances`` option:

::

    pegs mm10 --peaks PEAKSET [PEAKSET ...] --genes CLUSTER [CLUSTER ...] -d [DISTANCE [DISTANCE ...]]

For example:

::

    pegs mm10 --peaks ./InputPeaks/*.bed ./Clusters/*.txt -d 1000 2000

will calculate enrichments for +/-1KB and +/-2KB from the centre
of the input peak-set intervals.

.. warning::

   This is a change in version 0.6.0 to the previous way of
   specifying distances at the end of the command line, which
   is no longer supported.

Specifying TADs (``-t``, ``--tads``)
====================================

In addition to individual distances, enrichments within TADs
(Topologically Associated Domains) can be calculated by
providing a BED file with TAD definitions using the
``-t``/``--tads`` option.

In this case the heatmap for the TADs will be appended to the
heatmap for peaks and distances, and the raw data will be
appended to the XLSX file.

Specifying output file names (``--name``, ``-m``, ``-x``)
=========================================================

The basename for all the output files can be set using the
``--name`` option; by default the basename is ``pegs`` and
the output files will be called ``pegs_heatmap.png`` and
``pegs_results.xlsx``.

The names for these output files can also be set explicitly
using the ``-m`` and ``-x`` options:

 * ``-m``: sets the heatmap file name and image format
   (based on the file extension, e.g. ``my_heatmap.png``
   will produce a PNG image, ``my_heatmap.svg`` will
   produce an SVG etc)
 * ``-x``: sets the file name for the XLSX file

.. note::

   Using the ``-m`` and ``-x`` options to explicitly set
   the output file names will override the implicit file
   names generated from the basename.

Specifying where output files are written (``-o``)
==================================================

By default the result files are written to current working
directory, but they can be redirected to a different directory,
by using the ``-o`` option to specify the location.

.. note::

   The directory specified by ``-o`` will be created if it
   doesn't already exist.
