***********
Input files
***********

Reference gene intervals file
=============================

The reference gene intervals file contains the transcription
start sites (TSSs) for all genes as BED interval data.

There are two built-in gene interval BED files (``hg38`` and
``mm10``) which can be used by specifying the genome build names
as the ``GENE_INTERVAL_FILE``; otherwise a custom gene interval
file can be generated from refSeq data using the
:doc:`mk_pegs_intervals <mk_pegs_intervals>` utility.

Peak set files
==============

*TBA*

Gene cluster files
==================

The cluster files directory, are text files with lists of gene
names (one gene per line) which make up the cluster. They must
be named ``cluster_<NAME>.txt`` to be detected by the program.

TADS file
=========

*TBA*
