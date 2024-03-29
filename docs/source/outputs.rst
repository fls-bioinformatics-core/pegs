************
Output files
************

Overview
========

The default output of the program is a heatmap and the
corresponding data as an XLSX spreadsheet.

Heatmap
=======

In the heatmap, x-axis are the gene clusters, and y-axis show
peak-sets expanded to different genomic distances.

The cell color represents -log10(p-value) of enrichment, and
annotation of cells are the number of common genes for that
particular combination of gene cluster (x-axis) and gene-set
derived from the expanded peak-set (y-axis). For example:

.. image:: images/example_heatmap.png
   :width: 400
   :alt: Example heatmap from PEGS

If TADs are used, then the additional subplot at the bottom shows
similar enrichment as above, but without individual distances
for peak-sets (because each genomic interval is expanded to
distance/bounary defined in the TADs BED file). For example:

.. image:: images/example_with_tads_heatmap.png
   :width: 400
   :alt: Example heatmap with TADs from PEGS

Customising the heatmap
-----------------------

The heatmap colour palette is the default Seaborn 'cubehelix' palette
as generated by the ``seaborn.cubehelix_palette`` function:

 * https://seaborn.pydata.org/generated/seaborn.cubehelix_palette.html

A custom palette can be specified by using the ``--color`` option
to supply a base colour, for example:

::

    --color seagreen

Alternatively the palette can be fully specified by setting the
parameters supplied to ``seaborn.cubehelix_palette``, by using the
``--heatmap-palette`` option. For example, specifying:

::

    --heatmap-palette start=2 reverse=True

results in a "blue/green" heatmap with low values rendered as darker
and high values as lighter. Some other examples can be found at
https://seaborn.pydata.org/tutorial/color_palettes.html#sequential-cubehelix-palettes

As all the data used in the heatmap is also output to an XLSX file,
the user can use this to build their own custom heatmaps.

XLSX file
=========

This spreadsheet includes all the data (including p-values, and
common genes) used to generate the heatmap; for example:

.. image:: images/example_results_xlsx.png
   :width: 400
   :alt: Example XLSX output from PEGS

Optional outputs
================

Intersection files
------------------

By default the program removes all working data on successful
completion, however it is possible to keep the intermediate
intersection files by specifying the ``-k``
(``--keep-intersection-files``) option. The intersection files
will be written to the directory ``intersection_beds``.

These files are generated by intersecting the expanded peak-set
BED file (for a given distance) and the ``GENE_INTERVALS`` input
file (reference gene intervals file for all genes). They can be
used for further analysis, for example finding common gene names
and overlapping peaks, which can be used for motif enrichment etc.

Raw p-value and count data
--------------------------

These can be output using the ``--dump-raw-data`` option.
