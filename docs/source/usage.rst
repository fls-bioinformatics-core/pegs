**************************
Running analyses with PEGS
**************************

Basic usage
===========

To run an analysis the basic command line is:

::

    pegs [options] GENE_INTERVALS PEAKS_DIR CLUSTERS_DIR

where:

 * ``GENE_INTERVALS`` is a set of reference transcription
   start sites (TSSs) for all genes; it can either be the
   name of a built-in reference set (for example "mm10"),
   or file with BED interval data
 * ``PEAKS_DIR`` is a directory with input BED files
   containing the ChIP-seq (or other genomic intervals) peaks
   data (one peak-set per file)
 * ``CLUSTERS_DIR`` is a directory containing the files
   defining the gene clusters

``PEGS`` will then calculate the enrichments (p-values and
counts) using a default set of genomic distances around the
input intervals in each of the peak-sets.

By default the program outputs a heatmap PNG called
``pegs_heatmap.png``, and an XLSX file with the p-values and
count data called ``pegs_results.xlsx``.

The formats and naming conventions for the various files are
described in :doc:`inputs` and :doc:`outputs`.

Specifying genomic distances
============================

The default set of genomic distances used in the enrichment
calculations can be overriden with a custom set of intervals
specified at the end of the command line:

::

    pegs mm10 ./InputPeaks/ ./Clusters/ [DISTANCE [DISTANCE ...]]

For example:

::

    pegs mm10 ./InputPeaks/ ./Clusters/ 1000 2000

will calculate enrichments for +/-1KB and +/-2KB from the centre
of the input peak-set intervals.

Specifying TADs (``-t``, ``--tads``)
====================================

Enrichments for TADs (topologically associating domains) can
be calculated by providing a BED file with TAD definitions
using the ``-t``/``--tads`` option.

In this case the heatmap for the TADs will be appended to the
heatmap for peaks and distances, and the raw data will be
appended to the XLSX file.

Specifying output file names (``--name``, ``-m``, ``-x``)
=========================================================

The basename for the output files can be set using the
``--name`` option; by default the basename is ``pegs`` and
the output files will be called ``pegs_heatmap.png`` and
``pegs_results.xlsx``.

The names for these output files can also be set explicitly
using the ``-m`` option (sets the file name for the heatmap)
and ``-x`` option (sets the file name for the XLSX file).

Specifying where output files are written (``-o``)
==================================================

By default the result files are written to current working
directory, but they can be redirected to a different directory,
by using the ``-o`` option to specify the location.

.. note::

   The directory specified by ``-o`` will be created if it
   doesn't already exist.
