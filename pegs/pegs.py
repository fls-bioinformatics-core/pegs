#!/usr/bin/env python
#
#     pegs.py: core functionality for Peak-set Enrichment of Gene-Sets
#     Copyright (C) University of Manchester 2018-2021 Mudassar Iqbal, Peter Briggs
#

#######################################################################
# Imports
#######################################################################

from builtins import str
import sys
import os
import io
import glob
import numpy as np
import subprocess
import tempfile
import shutil
import logging

from scipy.stats import hypergeom as hg

from os import getcwd
from os import mkdir

from os.path import join
from os.path import basename
from os.path import abspath
from os.path import splitext
from os.path import exists

from .bedtools import intersect
from .outputs import make_heatmap
from .outputs import make_xlsx_file
from .outputs import write_raw_data
from .utils import count_genes
from .utils import intersection_file_basename

#######################################################################
# Constants
#######################################################################

# P-value cap
MIN_PVALUE = 1e-12

#######################################################################
# Functions
#######################################################################

def make_expanded_bed(bed_file,expanded_bed_file,interval):
    """
    Extends the start and end positions by the supplied
    interval distance

    Inputs:
    - bed_file (str): input BED file to expand
    - expanded_bed_file (str): output expanded BED file
    - interval (int): distance to extend start and end by
    """
    with io.open(bed_file,"rt") as bed:
        with io.open(expanded_bed_file,"wt") as expanded:
            for line in bed:
                s=line.split()
                # Stops reading if an empty line is encountered
                if not s:
                    break
                # Expand the interval
                s[1] = str(max(int(s[1])-interval,0))
                s[2] = str(max(int(s[2])+interval,0))
                # Reassemble the line and write out
                expanded.write("%s\n" % '\t'.join(s))
    return expanded_bed_file

def get_overlapping_genes(genes_file,peaks_file,interval=None,
                          report_entire_feature=False,
                          working_dir=None,bedtools_exe="bedtools"):
    """
    Find genes overlapping ChIP-seq peaks

    Returns the set of unique genes which overlap with the
    peaks for the supplied interval distance

    genes_file (str): path to BED file with all genes
    interval (int): distance to calculate overlaps for
    peaks_file (list): BED file containing the ChIP-seq peaks
    report_entire_feature (bool): if True then run intersectBed
    with the -wa option (to report the entire feature, not just
    the overlap)
    bedtools_exe (str): 'bedtools' executable to use
    """
    # Working directory
    if working_dir is None:
        wd = getcwd()
    else:
        wd = abspath(working_dir)
    # Base name for output files
    output_basename = intersection_file_basename(genes_file,
                                                 peaks_file,
                                                 interval)
    # If interval isn't explicitly set then assume zero
    if interval is None:
        interval = 0
    # Create "expanded" BED file for use with 'intersectBed'
    if interval > 0:
        expanded_bed_file = join(wd,"%s_Expanded.bed" % output_basename)
        make_expanded_bed(peaks_file,expanded_bed_file,interval)
    else:
        # Interval distance is zero so no expansion necessary
        expanded_bed_file = peaks_file
    # Intersect gene promoters
    intersection_file = join(wd,"Intersection.%s.bed" % output_basename)
    intersect(genes_file,expanded_bed_file,intersection_file,
              working_dir=wd,report_entire_feature=report_entire_feature,
              bedtools_exe=bedtools_exe)
    # Read data from intersection file to get unique list of genes
    # (across all genome) which are overlapping with ChIPseq peaks for
    # this interval
    # NB lines in intersection file look like e.g.:
    # chr13	21875265	21875266	ENSMUSG00000075032.3
    # i.e. gene is in 4th column
    genes = set()
    with io.open(intersection_file,'rt') as fp:
        for line in fp:
            genes.add(line.rstrip().split('\t')[3])
    return genes

def get_tads_overlapping_peaks(tads_file,peaks_file,tads_subset_file,
                               working_dir=None,bedtools_exe="bedtools"):
    """
    Get subset of TADs overlapping peaks

    Inputs:
    - tads_file (str): BED file with TADs
    - peaks_file (str): BED file with peaks
    - tads_subset_file (str): path to output BED file with TADs
      overlapping with the peaks
    - working_dir (str): (optional) working directory to use for
      intermediate files (defaults to CWD)
    - bedtools_exe (str): 'bedtools' executable to use
    """
    intersect(tads_file,peaks_file,tads_subset_file,
              working_dir=working_dir,report_entire_feature=True,
              bedtools_exe=bedtools_exe)
    return tads_subset_file

def calculate_enrichment(genes_file,peaks_file,clusters,n_genes,working_dir,
                         distance=None,report_entire_feature=False,
                         bedtools_exe="bedtools"):
    """
    Calculate enrichment for a single peak set and distance

    genes_file (str): path to BED file with all genes
    distance (int): distance to calculate enrichments at
    peaks_file (list): BED file containing the ChIP-seq peaks
    clusters (list): cluster files
    n_genes (int): total number of genes in the genes BED file
    report_entire_feature (bool): if True then run intersectBed
    with the -wa option (to report the entire feature, not just
    the overlap)
    bedtools_exe (str): 'bedtools' executable to use

    Returns tuple (pvalue,counts) i.e. col1 for p-val, col2 for
    number of genes)
    """
    # Initialise result arrays
    pvalues = np.zeros([len(clusters)])
    counts = np.zeros([len(clusters)])
    # Get set of genes overlapping this peak set for this distance
    overlap_genome = get_overlapping_genes(genes_file,peaks_file,distance,
                                           working_dir=working_dir,
                                           report_entire_feature=
                                           report_entire_feature)
    # Find subsets of overlapping genes in each RNA-seq cluster
    # and calculate enrichments
    for i,cluster_file in enumerate(clusters):
        # Read cluster file
        genes_cls = set(np.loadtxt(cluster_file,
                                   delimiter='\t',
                                   ndmin=1,
                                   usecols=[0],
                                   dtype=np.str))
        # No. of genes in current cluster (sample size)
        n = len(genes_cls)
        # Total number of overlapping genes (for set of all genes)
        K_i = len(overlap_genome)
        # Genes from the input regions based set, which are also in this cluster
        n_i = len(overlap_genome.intersection(genes_cls))
        # Calculate and store enrichment from hypergeometric function
        pvalues[i] = max(MIN_PVALUE,1.0 - hg.cdf(n_i-1,n_genes,n,K_i))
        counts[i] = n_i
    return (pvalues,counts)

def calculate_enrichments(genes_file,distances,peaks,clusters,tads_file,
                          keep_intersection_files=False,
                          output_directory=None,bedtools_exe="bedtools"):
    """
    Calculate enrichments for all ChIP-seq peak files and distances

    genes_file (str): path to BED file with all genes
    distances (list): list of distances to calculate enrichments at
    peaks (list): BED files containing the ChIP-seq peaks
    clusters (list): cluster files
    tads_file (str): path to BED file with TADs
    keep_intersection_files (bool): if True then keep the intermediate
      intersection files from bedtools
    output_directory (str): path to output directory (only used if
       keeping intersection files)
    bedtools_exe (str): 'bedtools' executable to use
    """
    # Temporary working directory
    working_dir = tempfile.mkdtemp(prefix="__LocalBeds.",dir=getcwd())

    # Count total number of genes
    n_genes = count_genes(genes_file)

    # Convenience variables
    n_peaks = len(peaks)
    n_clusters = len(clusters)
    n_distances = len(distances)

    # Storage for results
    pvalues = np.zeros([n_peaks,n_distances,n_clusters])
    counts = np.zeros([n_peaks,n_distances,n_clusters])

    # Calculate enrichments for all peaks, distances and clusters
    for i,peaks_file in enumerate(peaks):
        print("-- Processing peaks for %s" % basename(peaks_file))
        for j,distance in enumerate(distances):
            enrichment = calculate_enrichment(genes_file,peaks_file,
                                              clusters,n_genes,
                                              distance=distance,
                                              working_dir=working_dir,
                                              bedtools_exe=bedtools_exe)
            pvalues[i,j,:] = enrichment[0][:]
            counts[i,j,:] = enrichment[1][:]
    print("")

    # Handle TADs
    if tads_file:
        # Storage for TADs enrichments
        tads_pvalues = np.zeros([n_peaks,n_clusters])
        tads_counts = np.zeros([n_peaks,n_clusters])
        # Calculate enrichments for TADs
        for i,peaks_file in enumerate(peaks):
            print("-- Processing TADS for %s" % basename(peaks_file))
            # Get the subset of TADs which overlap with these peaks
            tads_subset = join(working_dir,
                               "%s.%s.bed" %
                               (splitext(basename(peaks_file))[0],
                                splitext(basename(tads_file))[0]))
            get_tads_overlapping_peaks(tads_file,peaks_file,tads_subset,
                                       bedtools_exe=bedtools_exe)
            # Calculate enrichments for the subset of TADs
            enrichment = calculate_enrichment(genes_file,tads_subset,
                                              clusters,n_genes,
                                              working_dir=working_dir,
                                              report_entire_feature=True)
            tads_pvalues[i,:] = enrichment[0][:]
            tads_counts[i,:] = enrichment[1][:]
        print("")
    else:
        tads_pvalues = None
        tads_counts = None

    # Copy the intersection files
    if keep_intersection_files:
        print("====Copying intersection BED files====\n")
        intersections_dir = "intersection_beds"
        if output_directory is not None:
            intersections_dir = os.path.join(output_directory,
                                             intersections_dir)
        if not exists(intersections_dir):
            mkdir(intersections_dir)
        for f in glob.glob(join(working_dir,"Intersection.*.bed")):
            ff = join(intersections_dir,basename(f))
            shutil.copyfile(f,ff)

    # Remove the working directory
    shutil.rmtree(working_dir)

    # Return the enrichment data
    return (pvalues,counts,tads_pvalues,tads_counts)

def pegs_main(genes_file,distances,peaks,clusters,
              tads_file,name,heatmap=None,xlsx=None,
              output_directory=None,
              keep_intersection_files=False,
              clusters_axis_label=None,peaksets_axis_label=None,
              heatmap_cmap=None,heatmap_format=None,
              bedtools_exe="bedtools",dump_raw_data=False):
    """
    Driver function for enrichment calculation

    Arguments:
      genes_file (str): path to BED file with all genes
      distances (list): list of distances to calculate enrichments at
      peaks (list): list of BED files containing the ChIP-seq peaks
      clusters (list): list of cluster files
      tads_file (str): path to BED file with TADs
      name (str): basename to use for output files
      heatmap (str): path for output heatmap image file
      xlsx (str): path for output XLSX file with raw data
      output_directory (str): directory to write output files to
        (defaults to current directory if not specified)
      keep_intersection_files (bool): if True then keep the intermediate
        intersection files from bedtools
      clusters_axis_label (str): custom label for the x-axis
      peaksets_axis_label (str): custom label for the y-axis
      heatmap_cmap (cmap): non-default colormap to use when creating
        the heatmaps
      heatmap_format (str): image format for output heatmaps
      bedtools_exe (str): 'bedtools' executable to use
      dump_raw_data (bool): if True then save the raw enrichment data
        to file (for debugging purposes)
    """
    # Path to BED with all genes
    genes_file = abspath(genes_file)
    print("====Genes interval file====")
    print("%s\n" % genes_file)
    if not exists(genes_file):
        logging.fatal("Genes interval file not found: %s" %
                      genes_file)
        return

    # Report the peak files
    print("====Peaks Files====")
    if not peaks:
        logging.fatal("No peaks files supplied")
        return
    for f in peaks:
        print("%s" % basename(f))
    print("")

    # Report the cluster files
    print("====Cluster Files====")
    if not clusters:
        logging.fatal("No cluster files supplied")
        return
    for f in clusters:
        print("%s" % basename(f))
    print("")

    # Path to TADs file (if supplied)
    print("====TADs file====")
    if tads_file:
        tads_file = abspath(tads_file)
        print("%s" % tads_file)
    else:
        print("Not supplied")
    print("")

    # Distances
    print("====Distances====")
    if not distances:
        logging.fatal("No distances specified")
        return
    for d in distances:
        print("%s" % d)
    print("")

    # Output directory
    if output_directory is None:
        output_directory = getcwd()
    output_directory = abspath(output_directory)
    if not exists(output_directory):
        mkdir(output_directory)

    # Path to the output heatmap
    if heatmap is None:
        if not heatmap_format:
            heatmap_format = "png"
        heatmap = "%s_heatmap.%s" % (name,heatmap_format)
    heatmap = os.path.join(output_directory,heatmap)

    # Path to the output XLSX
    if xlsx is None:
        xlsx = "%s_results.xlsx" % name
    xlsx = os.path.join(output_directory,xlsx)

    # Run the enrichment calculations
    print("====Starting analysis====")
    pvalues,counts,tads_pvalues,tads_counts = \
            calculate_enrichments(genes_file,distances,peaks,clusters,
                                  tads_file,
                                  keep_intersection_files=
                                  keep_intersection_files,
                                  output_directory=output_directory,
                                  bedtools_exe=bedtools_exe)

    # Plot the heatmap
    print("====Writing heatmap====")
    print("%s\n" % heatmap)
    make_heatmap(heatmap,peaks,clusters,distances,
                 pvalues,counts,tads_pvalues=tads_pvalues,
                 tads_counts=tads_counts,
                 clusters_axis_label=clusters_axis_label,
                 peaksets_axis_label=peaksets_axis_label,
                 heatmap_cmap=heatmap_cmap,
                 heatmap_format=heatmap_format)

    # Write data to spreadsheet
    print("====Writing XLSX file====")
    print("%s\n" % xlsx)
    make_xlsx_file(xlsx,peaks,clusters,distances,
                   pvalues,counts,tads_pvalues=tads_pvalues,
                   tads_counts=tads_counts)

    # Dump the 'raw' numbers for checking/debugging
    if dump_raw_data:
        print("====Dumping raw data to TSV files====\n")
        write_raw_data(name,peaks,clusters,distances,
                       pvalues,counts,tads_pvalues=tads_pvalues,
                       tads_counts=tads_counts,
                       output_directory=output_directory)
