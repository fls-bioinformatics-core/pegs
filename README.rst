**************************************
PEGS: Peak-set Enrichment of Gene-Sets
**************************************

``PEGS`` (**P**\ eak-set **E**\ nrichment of **G**\ ene-**S**\ ets) is
a Python bioinformatics utility for calculating enrichments of gene
clusters at different genomic distances from peaks.

* Free software: 3-Clause BSD License
* Documentation: https://pegs.readthedocs.io/en/latest/
* Code: https://github.com/fls-bioinformatics-core/pegs

-----------
Quick Start
-----------

The recommended way to get started with ``PEGS`` is to download
the latest version from the "releases" page on GitHub:

https://github.com/fls-bioinformatics-core/pegs/releases

and create a Python virtual environment, to install the software
into using the ``pip`` utility.

For example: to create and activate a virtual environment called
``venv.pegs`` using the ``virtualenv`` utility:

::

    virtualenv venv.pegs
    source venv.pegs/bin/activate

The ``PEGS`` package can then be installed using ``pip``, for
example:

::

    pip install pegs-0.4.0.tgz

The simplest use of the program is:

::

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
