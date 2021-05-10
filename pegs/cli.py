#!/usr/bin/env python
#
#     cli.py: CLI for gene cluster enrichment analysis
#     Copyright (C) University of Manchester 2018-2020 Mudassar Iqbal, Peter Briggs
#
from builtins import str
import os
import argparse
import logging
# Deal with matplotlib backend before importing seaborn
# See https://stackoverflow.com/a/50089385/579925
import matplotlib
if os.environ.get('DISPLAY','') == '':
   print('No display found: using non-interactive Agg backend')
   matplotlib.use('Agg')
import seaborn as sns
import pathlib2
from .pegs import pegs_main
from .intervals import make_gene_interval_file
from .bedtools import fetch_bedtools
from .bedtools import bedtools_version
from .utils import find_exe
from . import get_version

# Description
PEGS_DESCRIPTION = "PEGS: Peak-set Enrichment of Gene-Sets"

# Default set of distances for enrichment calculation
DEFAULT_DISTANCES = [5000,25000,50000,100000,150000,200000]

# Built in gene interval files
BUILTIN_GENE_INTERVALS = {
    "hg38": "refGene_hg38_120719_intervals.bed",
    "mm10": "refGene_mm10_120719_intervals.bed",
}

# Types for cubehelix_palette options
CUBEHELIX_PALETTE_TYPES = {
    'n_colors': int,
    'start': float,
    'rot': float,
    'gamma': float,
    'hue': float,
    'dark': float,
    'light': float,
    'reverse': bool,
}

def pegs():
    # Create command line parser
    p = argparse.ArgumentParser(description=PEGS_DESCRIPTION)
    p.add_argument("gene_intervals",
                   metavar="GENE_INTERVALS",
                   help="either name of a built-in set of gene "
                   "intervals (%s), or a BED file with gene interval "
                   "data" %
                   ','.join(["'%s'" % x for x in BUILTIN_GENE_INTERVALS]))
    p.add_argument("peaks_dir",
                   metavar="PEAKS_DIR",
                   help="directory containing BED files with "
                   "peaks data")
    p.add_argument("clusters_dir",
                   metavar="CLUSTERS_DIR",
                   help="directory containing gene cluster files")
    p.add_argument("distances",metavar="DISTANCE",
                   action="store",
                   nargs="*",
                   default=None,
                   help="optionally specify distance(s) to calculate "
                   "enrichments for; if no distances are specified then "
                   "the default set will be used (i.e. %s)" %
                   ' '.join([str(x) for x in DEFAULT_DISTANCES]))
    p.add_argument('--version',action='version',version=get_version())
    p.add_argument("-t","--tads",metavar="TADS_FILE",
                   dest="tads_file",
                   action="store",
                   help="BED file with topologically associating "
                   "domains (TADs)")
    output_options = p.add_argument_group("Output options")
    output_options.add_argument("--name",metavar="BASENAME",
                                dest="name",
                                action='store',
                                default="pegs",
                                help="basename for output files (default: "
                                "'pegs')")
    output_options.add_argument("-o",metavar="OUTPUT_DIRECTORY",
                                dest="output_directory",
                                action="store",
                                default=None,
                                help="specify directory to write output "
                                "files to (default: write to current "
                                "directory)")
    output_options.add_argument("-m",metavar="HEATMAP",
                                dest="output_heatmap",
                                action="store",
                                default=None,
                                help="destination for output heatmap PNG "
                                "(default: 'BASENAME_heatmap.png')")
    output_options.add_argument("-x",metavar="XLSX",
                                dest="output_xlsx",
                                action="store",
                                default=None,
                                help="destination for output XLSX file "
                                "with the raw enrichment data (default: "
                                "'BASENAME_results.xlsx')")
    heatmap_options = p.add_argument_group("Heatmap options")
    g = heatmap_options.add_mutually_exclusive_group()
    g.add_argument("--color",
                   dest="heatmap_color",
                   metavar="COLOR",
                   action="store",
                   default=None,
                   help="specify a base color to use for the heatmap "
                   "(NB not compatible with --heatmap-palette)")
    g.add_argument("--heatmap-palette",
                   dest="heatmap_palette_options",
                   metavar="OPTION=VALUE",
                   action="store",
                   nargs="+",
                   default = None,
                   help="advanced option to specify custom palette "
                   "settings for the output heatmap (e.g. 'start=0.5', "
                   "'rot=0' etc). Available options are those listed in "
                   "the 'cubehelix_palette' documentation at "
                   "https://seaborn.pydata.org/generated/"
                   "seaborn.cubehelix_palette.html (NB not compatible "
                   "with --color)")
    advanced_options = p.add_argument_group("Advanced options")
    advanced_options.add_argument("-k","--keep-intersection-files",
                                  dest="keep_intersection_files",
                                  action="store_true",
                                  help="keep the intermediate intersection "
                                  "files (useful for debugging)")
    advanced_options.add_argument("--dump-raw-data",
                                  dest="dump_raw_data",
                                  action="store_true",
                                  help="dump the raw data (gene counts and "
                                  "p-values) to TSV files (for debugging)")
    args = p.parse_args()
    # Generate list of distances
    if not args.distances:
        # Defaults
        distances = [d for d in DEFAULT_DISTANCES]
    else:
        # Assemble from command line
        distances = list()
        for d in args.distances:
            for x in d.split(','):
                distances.append(int(x))
    distances = sorted(distances)
    # Check if using built-in interval data
    gene_interval_file = args.gene_intervals
    try:
        gene_interval_file = BUILTIN_GENE_INTERVALS[gene_interval_file]
        p = os.path.dirname(__file__)
        while p != os.sep:
            f = os.path.join(p,"pegs-%s" % get_version(),gene_interval_file)
            if os.path.exists(f):
                gene_interval_file = f
                break
            else:
                p = os.path.dirname(p)
    except KeyError:
        # Not found, ignore
        pass
    # Build colormap for heatmap
    heatmap_cmap = None
    if args.heatmap_color:
        # Construct non-default colormap using the
        # seaborn lightpalette function
        heatmap_cmap = sns.light_palette(color=args.heatmap_color,
                                         as_cmap=True)
    elif args.heatmap_palette_options is not None:
        # Construct non-default colormap using the
        # options supplied by the user
        heatmap_palette_options = {
            'n_colors': 6,
            'start': 0,
            'rot': 0.4,
            'gamma': 1.0,
            'hue': 0.8,
            'light': 0.85,
            'dark': 0.15,
            'reverse': False,
        }
        for o in args.heatmap_palette_options:
            key,value = o.split("=")
            if key not in heatmap_palette_options:
                logging.warning("Unrecognised palette option: '%s'"
                                % key)
            else:
                heatmap_palette_options[key] = \
                        CUBEHELIX_PALETTE_TYPES[key](value)
        heatmap_cmap = sns.cubehelix_palette(as_cmap=True,
                                             **heatmap_palette_options)
    # Report version and authors etc
    print("%s %s" % (PEGS_DESCRIPTION,get_version()))
    print("""
Efficiently calculate enrichments of gene clusters in
multiple genomic intervals data (e.g. ChIP-seq peak-sets)
at different distances

Copyright University of Manchester
Faculty of Biology Medicine and Health
Authors: Mudassar Iqbal, Peter Briggs
""")

    # Add PEGS 'bin' directory in user's home area to PATH
    # NB this might not exist
    pegs_dir = os.path.join(str(pathlib2.Path.home()),".pegs")
    pegs_bin_dir = os.path.join(pegs_dir,"bin")
    os.environ['PATH'] = "%s%s%s" % (os.environ['PATH'],
                                     os.pathsep,
                                     pegs_bin_dir)

    # Locate bedtools executable
    bedtools_exe = find_exe("bedtools")
    if not bedtools_exe:
        # Not found
        logging.warning("'bedtools' not found")
        # Attempt to get bedtools
        bedtools_exe = fetch_bedtools(install_dir=pegs_bin_dir,
                                      create_install_dir=True)
        if not bedtools_exe:
            logging.fatal("Failed to fetch 'bedtools'")
            return 1
    print("Found %s (%s)\n" % (bedtools_version(bedtools_exe),
                               bedtools_exe))

    # Calculate the enrichments
    pegs_main(genes_file=gene_interval_file,
              distances=distances,
              peaks_dir=args.peaks_dir,
              clusters_dir=args.clusters_dir,
              tads_file=args.tads_file,
              name=args.name,
              heatmap=args.output_heatmap,
              xlsx=args.output_xlsx,
              output_directory=args.output_directory,
              keep_intersection_files=
              args.keep_intersection_files,
              heatmap_cmap=heatmap_cmap,
              dump_raw_data=args.dump_raw_data)

def mk_pegs_intervals():
    # Create command line parser
    p = argparse.ArgumentParser()
    p.add_argument("refgene_file",
                   metavar="REFGENE_FILE",
                   help="refGene annotation data for the genome "
                   "of interest")
    p.add_argument("gene_interval_file",
                   metavar="GENE_INTERVAL_FILE",
                   nargs='?',
                   help="destination for output BED file with "
                   "gene interval data (default: "
                   "'<REFGENE_FILE>_intervals.bed')")
    p.add_argument('--version',action='version',version=get_version())
    args = p.parse_args()
    # Report version
    print("MK_PEGS_INTERVALS %s\n" % get_version())
    # Generate the gene interval file
    make_gene_interval_file(args.refgene_file,
                            args.gene_interval_file)
