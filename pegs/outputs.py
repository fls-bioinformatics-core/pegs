#!/usr/bin/env python
#
#     outputs.py: functions for outputting result data
#     Copyright (C) University of Manchester 2018-2021 Mudassar Iqbal, Peter Briggs
#

#######################################################################
# Constants
#######################################################################

# Default axis labels
CLUSTERS_AXIS_LABEL = "RNA-seq Clusters"
PEAKSETS_AXIS_LABEL = "Peak Sets and Intervals"
# Sets font size for heatmap annotation
ANNOTATION_FONT_SIZE = 16
# Sets font size for peakset names associated with distances
# on y-axis
PEAKSET_LABEL_FONT_SIZE = 16
# Sets font size for tick labels on all x- and y-axes
X_TICK_LABEL_FONT_SIZE = 16
Y_TICK_LABEL_FONT_SIZE = 16
# Sets font size for the x- and y-axes labels
AXIS_LABEL_FONT_SIZE = 24

#######################################################################
# Imports
#######################################################################

from builtins import str
import io
import os
import numpy as np
# Deal with matplotlib backend
# See https://stackoverflow.com/a/50089385/579925
import matplotlib
if os.environ.get('DISPLAY','') == '':
   print('No display found: using non-interactive Agg backend')
   matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import xlsxwriter

from os.path import basename
from os.path import splitext

#######################################################################
# Functions
#######################################################################

def make_heatmap(heatmap_file,peaks,clusters,distances,pvalues,counts,
                 tads_pvalues=None,tads_counts=None,
                 clusters_axis_label=None,
                 peaksets_axis_label=None,
                 heatmap_cmap=None,heatmap_format=None):
    """
    Generate a heatmap from enrichment data

    Arguments:
      heatmap_file (str): name/path for output heatmap PNG
      peaks (list): BED files containing the ChIP-seq peaks
      clusters (list): list of distances to calculate enrichments at
      distances (list): cluster files
      pvalues (numpy.array): Numpy array with pvalues from enrichment
        calculation
      counts (numpy.array): Numpy array with gene counts from enrichment
        calculation
      tads_pvalues (numpy.array): Numpy array with TADs pvalues from
        enrichment calculation (None if TADs not included)
      tads_counts (numpy.array): Numpy array with TADs gene counts
        from enrichment calculation (None if TADs not included)
      clusters_axis_label (str): custom label for the x-axis
      peaksets_axis_label (str): custom label for the y-axis
      heatmap_cmap (cmap): optional, colormap to use when plotting
        the heatmaps
      heatmap_format (str): optional, image format for output heatmaps
    """
    # Defaults for axis labels
    if clusters_axis_label is None:
       clusters_axis_label = CLUSTERS_AXIS_LABEL
    if peaksets_axis_label is None:
       peaksets_axis_label = PEAKSETS_AXIS_LABEL

    # Convenience variables
    n_peaks = len(peaks)
    n_clusters = len(clusters)
    n_distances = len(distances)
    include_tads = (tads_pvalues is not None) and \
                   (tads_counts is not None)

    # Make '2d' versions of enrichment data for plotting heatmap
    pvalues_2d = np.zeros([n_peaks*n_distances,n_clusters])
    counts_2d = np.zeros([n_peaks*n_distances,n_clusters])
    for i,peaks_file in enumerate(peaks):
        for j,distance in enumerate(distances):
            x = i*n_distances + j
            pvalues_2d[x,:] = pvalues[i,j,:]
            counts_2d[x,:] = counts[i,j,:]

    # Min/max pvalues for colorbar
    min_pvalue = np.amin(-np.log10(pvalues_2d))
    max_pvalue = np.amax(-np.log10(pvalues_2d))
    if include_tads:
        min_pvalue = min(min_pvalue,np.amin(-np.log10(tads_pvalues)))
        max_pvalue = max(max_pvalue,np.amax(-np.log10(tads_pvalues)))

    # Xlabel (cluster names)
    xlbls = [os.path.splitext(os.path.basename(x))[0]
             for x in clusters]

    # Ylabel (interval distances repeated for each peak set)
    ylbls = [d for d in distances] * n_peaks

    # Set up grid and axes for plotting the heatmaps and
    # associated colorbars
    # (see https://stackoverflow.com/a/45645152)
    if include_tads:
        # 2 x 2 grid to include TADS
        fig,axes = plt.subplots(2,2,
                                gridspec_kw={
                                    'height_ratios': [5,1],
                                    'width_ratios': [30,1],
                                    'hspace': 0.1,
                                    'wspace': 0.05,
                                })
        # Axes for main heatmap and colorbar
        ax = axes[0][0]
        cbar_ax = axes[0][1]
        # Axes for TADs heatmap and colorbar
        tads_ax = axes[1][0]
        tads_cbar_ax = axes[1][1]
    else:
        # 1 x 2 grid (no TADS)
        fig,axes = plt.subplots(1,2,
                                gridspec_kw={
                                    'height_ratios': [5],
                                    'width_ratios': [30,1],
                                    'hspace': 0.1,
                                    'wspace': 0.05,
                                })
        # Axes for main heatmap and colorbar
        ax = axes[0]
        cbar_ax = axes[1]

    # Set to the size of A4 paper
    fig.set_size_inches(20.7, 20.27)

    # Set up default colormap if none was supplied
    if heatmap_cmap is None:
        heatmap_cmap = sns.cubehelix_palette(as_cmap=True)

    # Plot the heatmap
    sns.heatmap(data=-np.log10(pvalues_2d),
                ax=ax,
                linewidths=0.3,
                linecolor='lightblue',
                xticklabels=xlbls,
                yticklabels=ylbls,
                annot=counts_2d,
                annot_kws={
                    "size": ANNOTATION_FONT_SIZE,
                },
                fmt = 'g',
                vmin=min_pvalue,
                vmax=max_pvalue,
                cbar=True,
                cbar_ax=cbar_ax,
                cbar_kws={
                    "orientation": "vertical",
                    "pad":0.03,
                    "fraction":0.05,
                    "label":"-log(Pval)",
                },
                cmap=heatmap_cmap)

    # Annotate the sets of distances in the heatmap
    # NB the coordinates are in the 'data' coordinate system
    # see https://matplotlib.org/tutorials/advanced/transforms_tutorial.html
    midpoint = n_distances/2.0
    xpos = n_clusters/10.0
    for i,peak_file in enumerate(peaks):
        name = splitext(basename(peak_file))[0]
        ypos = i*n_distances
        ax.text(-xpos,ypos+midpoint,
                name,
                ha="center",
                va="center",
                rotation=90,
                size=PEAKSET_LABEL_FONT_SIZE)
        ax.plot([-0.65*xpos,
                 -0.75*xpos,
                 -0.75*xpos,
                 -0.65*xpos],
                [ypos+0.1,
                 ypos+0.1,
                 ypos+n_distances-0.1,
                 ypos+n_distances-0.1],
                linewidth=2,clip_on=False,color="gray")

    # Label the axes and move y-label over to accommodate extra
    # annotation on y-axis
    # NB the coordinates are in the 'axes' coordinate system
    # see https://matplotlib.org/tutorials/advanced/transforms_tutorial.html
    ax.set_ylabel(peaksets_axis_label,
                  fontsize=AXIS_LABEL_FONT_SIZE)
    ax.get_yaxis().set_label_coords(-0.13,0.5)

    # Set the fontsize for the tick labels
    for tick in ax.xaxis.get_major_ticks():
        tick.label1.set_fontsize(X_TICK_LABEL_FONT_SIZE)
        tick.label1.set_rotation('horizontal')
    for tick in ax.yaxis.get_major_ticks():
        tick.label1.set_fontsize(Y_TICK_LABEL_FONT_SIZE)
        tick.label1.set_rotation('horizontal')

    # Deal with the colorbar
    cbar_ax.yaxis.label.set_size(AXIS_LABEL_FONT_SIZE)
    # Set the tick label size
    # (see https://stackoverflow.com/a/53095480)
    cbar_ax.tick_params(labelsize=Y_TICK_LABEL_FONT_SIZE)

    # TADs heatmap
    if include_tads:
        sns.heatmap(data=-np.log10(tads_pvalues),
                    ax=tads_ax,
                    linewidths=0.3,
                    linecolor='lightblue',
                    xticklabels=xlbls,
                    yticklabels=[splitext(basename(f))[0]
                                 for f in peaks],
                    annot=tads_counts,
                    annot_kws={
                        "size": ANNOTATION_FONT_SIZE,
                    },
                    fmt = 'g',
                    vmin=min_pvalue,
                    vmax=max_pvalue,
                    cbar=True,
                    cbar_ax=tads_cbar_ax,
                    cbar_kws={
                        "orientation": "vertical",
                        "pad":0.03,
                        "fraction":0.05,
                        "label":"-log(Pval)",
                    },
                    cmap=heatmap_cmap)
        tads_ax.get_yaxis().set_label_coords(-0.9,0.5)

        # Set the fontsize for the tick labels
        for tick in tads_ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(X_TICK_LABEL_FONT_SIZE)
            tick.label1.set_rotation('horizontal')
        for tick in tads_ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(Y_TICK_LABEL_FONT_SIZE)
            tick.label1.set_rotation('horizontal')

        # Colorbar
        tads_cbar_ax.yaxis.label.set_size(AXIS_LABEL_FONT_SIZE)
        tads_cbar_ax.tick_params(labelsize=Y_TICK_LABEL_FONT_SIZE)

    # Set x axis legend
    if include_tads:
        ax = tads_ax
    ax.set_xlabel(clusters_axis_label,fontsize=AXIS_LABEL_FONT_SIZE)

    # Save to file
    fig.savefig(heatmap_file,format=heatmap_format)

def make_xlsx_file(xlsx_file,peaks,clusters,distances,pvalues,counts,
                   tads_pvalues=None,tads_counts=None):
    """
    Generate an XLSX file from enrichment data

    Arguments:
      xlsx_file (str): name/path for output XLSX file
      peaks (list): BED files containing the ChIP-seq peaks
      clusters (list): list of distances to calculate enrichments at
      distances (list): cluster files
      pvalues (numpy.array): Numpy array with pvalues from enrichment
        calculation
      counts (numpy.array): Numpy array with gene counts from enrichment
        calculation
      tads_pvalues (numpy.array): Numpy array with TADs pvalues from
        enrichment calculation (None if TADs not included)
      tads_counts (numpy.array): Numpy array with TADs counts from
        enrichment calculation (None if TADs not included)
    """
    # Convenience variables
    n_peaks = len(peaks)
    n_clusters = len(clusters)
    n_distances = len(distances)
    include_tads = (tads_pvalues is not None) and \
                   (tads_counts is not None)
    cluster_names = [os.path.splitext(os.path.basename(x))[0]
                     for x in clusters]

    # Output workbook
    xlsx_out = xlsxwriter.Workbook(xlsx_file)

    # Make separate sheets for each set of values
    ws_common_genes = xlsx_out.add_worksheet("Common Genes")
    ws_p_values = xlsx_out.add_worksheet("P values")

    # Set up formats
    fmt_center = xlsx_out.add_format({'align':'center'})

    # Get widths of peak set names
    width = 0
    for peaks_file in peaks:
        width = max(width,len(basename(peaks_file)))

    # Make header rows
    for ws in (ws_common_genes,ws_p_values):
        ws.write(1,0,"Peak set")
        ws.write(1,1,"Interval")
        for k,cluster in enumerate(clusters):
            ws.write(1,k+2,cluster_names[k])
        ws.merge_range(0,2,0,n_clusters+1,
                       "Clusters",
                       fmt_center)

    # Write the data
    for i,peaks_file in enumerate(peaks):
        for j,distance in enumerate(distances):
            row = i*n_distances + j + 2
            ws_common_genes.write(row,0,basename(peaks_file))
            ws_common_genes.write(row,1,distance)
            ws_p_values.write(row,0,basename(peaks_file))
            ws_p_values.write(row,1,distance)
            for k,cluster in enumerate(clusters):
                ws_common_genes.write(row,k+2,counts[i,j,k])
                ws_p_values.write(row,k+2,pvalues[i,j,k])

    # Set the column width for peak sets
    ws_common_genes.set_column(0,0,width*1.2)
    ws_p_values.set_column(0,0,width*1.2)

    # Output TADs data if specified
    if include_tads:
        ws_tads_common_genes = xlsx_out.add_worksheet("Common Genes (TADs)")
        ws_tads_p_values = xlsx_out.add_worksheet("P values (TADs)")
        # Make header rows
        for ws in (ws_tads_common_genes,ws_tads_p_values):
            ws.write(0,0,"Peak set")
            for k,cluster in enumerate(clusters):
                ws.write(1,k+1,cluster_names[k])
                ws.merge_range(0,1,0,n_clusters,
                               "Clusters",
                               fmt_center)
        # Write the data
        for i,peaks_file in enumerate(peaks):
            row = i+1
            ws_tads_common_genes.write(row,0,basename(peaks_file))
            ws_tads_p_values.write(row,0,basename(peaks_file))
            for k,cluster in enumerate(clusters):
                ws_tads_common_genes.write(row,k+1,tads_counts[i,k])
                ws_tads_p_values.write(row,k+1,tads_pvalues[i,k])
    # Set the column width for peak sets
    ws_common_genes.set_column(0,0,width*1.2)
    ws_p_values.set_column(0,0,width*1.2)
    if include_tads:
        ws_tads_common_genes.set_column(0,0,width*1.2)
        ws_tads_p_values.set_column(0,0,width*1.2)
    xlsx_out.close()

def write_raw_data(name,peaks,clusters,distances,pvalues,counts,
                   tads_pvalues=None,tads_counts=None,
                   output_directory=None):
    """
    Write the raw pvalue/count data to tab-delimited files

    Arguments:
      name (str): basename to use for output files
      peaks (list): BED files containing the ChIP-seq peaks
      clusters (list): list of distances to calculate enrichments at
      distances (list): cluster files
      pvalues (numpy.array): Numpy array with pvalues from enrichment
        calculation
      counts (numpy.array): Numpy array with gene counts from enrichment
        calculation
      tads_pvalues (numpy.array): Numpy array with TADs pvalues from
        enrichment calculation (None if TADs not included)
      tads_counts (numpy.array): Numpy array with TADs gene counts from
        enrichment calculation (None if TADs not included)
      output_directory (str): output directory to write files to (will
        be current working directory if not supplied)
    """
    # Convenience variables
    include_tads = (tads_pvalues is not None) and \
                   (tads_counts is not None)

    # Output directory
    if output_directory is None:
        output_directory = os.getcwd()
    output_directory = os.path.abspath(output_directory)

    # Dump pvalues and gene counts
    pval_filen = os.path.join(output_directory,'%s_pval.tsv' % name)
    count_filen = os.path.join(output_directory,'%s_count.tsv' % name)
    with io.open(pval_filen,'wt') as fpval:
        with io.open(count_filen,'wt') as fcount:
            for i,peaks_file in enumerate(peaks):
                for j,distance in enumerate(distances):
                    line_pval = [basename(peaks_file),distance]
                    line_count = [basename(peaks_file),distance]
                    for k,cluster in enumerate(clusters):
                        line_pval.append(pvalues[i,j,k])
                        line_count.append(int(counts[i,j,k]))
                    fpval.write("%s\n" % '\t'.join([str(x) for x in line_pval]))
                    fcount.write("%s\n" % '\t'.join([str(x) for x in line_count]))

    # Dump data for TADs
    if include_tads:
        tads_pval_filen = os.path.join(output_directory,
                                       '%s_tads_pval.tsv' % name)
        tads_count_filen = os.path.join(output_directory,
                                        '%s_tads_count.tsv' % name)
        with io.open(tads_pval_filen,'wt') as fpval:
            with io.open(tads_count_filen,'wt') as fcount:
                for i,peaks_file in enumerate(peaks):
                    line_pval = [basename(peaks_file)]
                    line_count = [basename(peaks_file)]
                    for k,cluster in enumerate(clusters):
                        line_pval.append(tads_pvalues[i,k])
                        line_count.append(int(tads_counts[i,k]))
                    fpval.write("%s\n" % '\t'.join([str(x) for x in line_pval]))
                    fcount.write("%s\n" % '\t'.join([str(x) for x in line_count]))
