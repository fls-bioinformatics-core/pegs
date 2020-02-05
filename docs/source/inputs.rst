***********
Input files
***********

Reference gene intervals file
=============================

The gene intervals file contains the  reference transcription
start sites (TSSs) for all genes as BED interval data.

There are two built-in gene interval BED files (``hg38`` and
``mm10``) which have been generated from the refGene data
downloaded from the UCSC table browser on 12th July 2019.
These can be used when running ``PEGS`` by specifying the genome
build names on the command line.

Otherwise a custom gene interval file must be generated from refSeq
data using the :doc:`mk_pegs_intervals <mk_pegs_intervals>` utility.

Peak set files
==============

Peak-set files are BED files containing ChIP-seq peaks or other
genomic interval data of interest.

The files need to contain three columns with chromosome, start
and end positions, for example:

::

    chr1	39756959	39757488
    chr1	40278922	40279363
    chr1	49032761	49033125
    ...

The names of the files are used as identifiers in the ouput XLSX
and heatmap plot files.

Gene cluster files
==================

The gene cluster files are text files with lists of gene names (one gene
per line) which make up the cluster, for example:

::

    Ahctf1
    Aif1l
    Amd1
    Asnsd1
    ...

They must be named ``cluster_NAME.txt`` to be detected by the
program; the ``NAME``\s are used as identifiers in the output
XLSX and heatmap plot files.

TADs file
=========

The TADs (topologically associating domains) file is a BED file
containing intervals which defines a set of TAD boundaries to be
used in a supplementary enrichment analysis. This supplementary
analysis uses the TAD intervals instead of the genomic distances.

The files need to contain four columns with chromosome, start and
end positions, and a name, for example:

::

    chr1	3009919	4369919	TAD1
    chr1	4369919	4769919	TAD2
    chr1	4769919	6209919	TAD3
    ...

The TAD names are used as identifiers in the output XLSX and
heatmap plot files.
