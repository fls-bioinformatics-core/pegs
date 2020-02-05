**************************
Running analyses with PEGS
**************************

Basic usage
===========

To run an analysis the basic command line is:

::

    pegs [options] GENE_INTERVALS PEAKS_DIR CLUSTERS_DIR

where:

 * ``GENE_INTERVAL_FILE`` is a text file with transcription
   start sites (TSSs) for all genes as BED interval data
 * ``PEAKS_DIR`` is a directory with input BED files containing
   the ChIP-seq (or other genomic intervals) peaks data
 * ``CLUSTERS_DIR`` is a directory containing file(s) for
   gene clusters

By default the program outputs a heatmap PNG called
``pegs_heatmap.png``, and an XLSX file with the p-values and
count data called ``pegs_results.xlsx``.

Specifying genomic distances
============================

PEGS will calculate the enrichments using a default set of
genomic distances around the input intervals, but these can be
overriden by a custom set of intervals specified at the end
of the command line:

::

    pegs mm10 ./InputPeaks/ ./Clusters/ [DISTANCE [DISTANCE ...]]

For example:

::

    pegs mm10 ./InputPeaks/ ./Clusters/ 1000 2000

will calculate enrichments for +/-1KB and +/-2KB from the centre
of the input intervals.

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
