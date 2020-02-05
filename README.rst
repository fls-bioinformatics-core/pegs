**************************************
PEGS: Peak-set Enrichment of Gene-Sets
**************************************

``PEGS`` (**P**\ eak-set **E**\ nrichment of **G**\ ene-**S**\ ets) is
a Python bioinformatics utility for calculating enrichments of gene
cluster enrichments from peak data at different genomic distances.

-----------
Quick Start
-----------

Install the latest version of the program from the Python Package Index
(PyPI)::

    pip install pegs

The simplest use of the program is::

    pegs GENE_INTERVALS PEAKS_DIR CLUSTERS_DIR

where ``GENE_INTERVALS`` is a set of reference transcription
start sites (TSSs) for all genes, ``PEAKS_DIR`` is a directory
containing BED files with peak-sets, and ``CLUSTERS_DIR`` is a
directory containing files defining gene clusters.

This will output a PNG heatmap and an XLXS file with the
p-values and gene counts from the enrichment calculations.

Full documentation can be found at:

 * https://pegs.readthedocs.io/en/latest/

---------
Licensing
---------

*TBA*
