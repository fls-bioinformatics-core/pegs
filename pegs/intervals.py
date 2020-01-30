#!/usr/bin/env python
#
#     intervals.py: code to deal with interval files
#     Copyright (C) University of Manchester 2019-2020 Mudassar Iqbal, Peter Briggs
#

#######################################################################
# Imports
#######################################################################

from builtins import str
import os
import io
import logging
import numpy as np

#######################################################################
# Functions
#######################################################################

def make_gene_interval_file(refseq_file,
                            gene_interval_file=None,
                            verbose=False):
    """
    Create a gene interval BED file from refSeq data

    Arguments:
      refseq_file (str): file with refSeq annotation data
      gene_interval_file (str): destination for output gene
        interval data
      verbose (bool): if True then report duplicate gene
        names
    """
    gene_data = dict()
    duplicates = list()
    print("Reading in data from %s..." % refseq_file)
    with io.open(refseq_file,'rt') as refseq:
        for line in refseq:
            if line.startswith('#'):
                continue
            data = line.rstrip('\n').split()
            # Extract the name
            gene_name = data[12]
            if gene_name in gene_data:
                # Ignore duplicated names
                if verbose:
                    logging.warning(
                            "'%s': multiple occurrences "
                            "detected in annotation (only "
                            "first one will be kept)" %
                            gene_name)
                duplicates.append(gene_name)
                continue
            # Extract remaining data items
            chrom = data[2]
            start = int(data[4])
            stop = int(data[5])
            strand = data[3]
            # Sort the information for the gene
            gene_data[gene_name] = [chrom,start,stop,strand]
    print("Read %s genes (%s duplicated names ignored)" % (len(gene_data),
                                                           len(duplicates)))
    # Generate the gene interval BED file
    if not gene_interval_file:
        gene_interval_file = os.path.splitext(
            os.path.basename(refseq_file))[0] + "_intervals.bed"
    print("Writing gene intervals to %s..." % gene_interval_file)
    with io.open(gene_interval_file,'wt') as bed:
        for gene_name in sorted(list(gene_data)):
            # Look up the data for this gene
            chrom,start,stop,strand = gene_data[gene_name]
            # For '-' strand, flip start and stop
            if strand == '-':
                start = stop
            # Build the output line
            line = (chrom,
                    max(int(start),0),
                    max(int(start)+1,0),
                    gene_name)
            bed.write("%s\n" % '\t'.join([str(x) for x in line]))
    print("Done")
