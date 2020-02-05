**************************
Making gene interval files
**************************

The ``mk_pegs_intervals`` utility should be used to generate a
reference gene interval data file for input into the ``pegs``
analysis:

::

    mk_pegs_intervals REFGENE_FILE

where:

 * ``REFGENE_FILE`` is the refGene annotation data for the genome
   of interest

By default the output gene interval file will be called
``<REFGENE_FILE>_intervals.bed``; you can explicitly specify the
name using the ``-o`` option:

::

    mk_pegs_intervals refGene_mm10.txt -o refGene_mm10_120719_intervals.bed
