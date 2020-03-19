**************************
Making gene interval files
**************************

In order to work with other builds of human and mouse genome, or with
other organisms, the ``mk_pegs_intervals`` utility should be used to
generate a reference gene interval data file for input into the ``PEGS``
analysis:

::

    mk_pegs_intervals REFGENE_FILE

where:

 * ``REFGENE_FILE`` is the refGene annotation data for the genome
   of interest. These annotations can be obtained from UCSC table
   browser.

By default the output gene interval file will be called
``<REFGENE_FILE>_intervals.bed``; you can explicitly specify the
name using the ``-o`` option:

::

    mk_pegs_intervals refGene_mm10.txt -o refGene_mm10_120719_intervals.bed
