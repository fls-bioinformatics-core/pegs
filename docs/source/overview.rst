*************
What is PEGS?
*************

``PEGS`` (**P**\ eak-set **E**\ nrichment of **G**\ ene-**S**\ ets) is
a Python bioinformatics package for efficiently calculating enrichments
of gene clusters in multiple genomic intervals data (e.g. ChIP-seq
peak-sets) at different distances.

What it does
------------

Given input BED file(s), containing genomic intervals, coming from
ChIP-seq, ATAC-seq etc, and cluster(s) of genes for which user wants
to calculate enrichment, PEGS will expand each interval in the BED
file (from the centre, in both directions) for a given genomic distance,
and extract overlapping gene TSSs.

Using these genes, input gene cluster(s), and total number of genes in
the genome (RefSeq defined), PEGS will obtain the common genes (numbers
shown in the output heatmap cells), and corresponding hypergeometric
p-value (color in the output heatmap).

PEGS can very efficiently do this analysis for many peak-sets and gene
clusters at multiple genomic distances simultaneously and outputs the
result in a  combined, easy to interpret heatmap.

Citing PEGS
-----------

If you use PEGS in your research then please cite:

*  Briggs P, Hunter AL, Yang Sh et al.
   PEGS: An efficient tool for gene set enrichment within defined
   sets of genomic intervals [version 2; peer review: 2 approved].
   F1000Research 2021, 10:570
   (https://doi.org/10.12688/f1000research.53926.2)
