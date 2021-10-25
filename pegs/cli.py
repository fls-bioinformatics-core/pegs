#!/usr/bin/env python
#
#     cli.py: CLI for gene cluster enrichment analysis
#     Copyright (C) University of Manchester 2018-2021 Mudassar Iqbal, Peter Briggs
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
from .utils import collect_files
from .utils import sort_files
from . import get_version

# Description
PEGS_DESCRIPTION = "PEGS: Peak-set Enrichment of Gene-Sets"

# Citation
PEGS_CITATION = """
If you use PEGS in your research then please cite:

* Briggs P, Hunter AL, Yang Sh et al.
  PEGS: An efficient tool for gene set enrichment within defined
  sets of genomic intervals [version 1; peer review: 2 approved].
  F1000Research 2021, 10:570
  (https://doi.org/10.12688/f1000research.53926.1)
"""

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
    p.add_argument('--version',action='version',version=get_version())
    p.add_argument("-p","--peaks",
                   metavar="PEAK_SET_FILE",
                   dest="peaks",
                   action="store",
                   required=True,
                   nargs="+",
                   help="one or more input peak set files (BED format)")
    p.add_argument("-g","--genes",
                   metavar="GENE_CLUSTER_FILE",
                   dest="clusters",
                   action="store",
                   required=True,
                   nargs="+",
                   help="one or more input gene cluster files (one gene "
                   "per line)")
    p.add_argument("-t","--tads",metavar="TADS_FILE",
                   dest="tads_file",
                   action="store",
                   help="BED file with topologically associating "
                   "domains (TADs)")
    p.add_argument("-d","--distances",
                   metavar="DISTANCE",
                   dest="distances",
                   action="store",
                   nargs="+",
                   help="specify distance(s) to calculate enrichments "
                   "for (if no distances are specified then the default "
                   "set will be used i.e. %s)" %
                   ' '.join([str(x) for x in DEFAULT_DISTANCES]))
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
                                help="destination for output heatmap; "
                                "image format is implicitly determined by "
                                "the file extension (e.g. '.png','.svg' "
                                "etc) unless overridden by the --format "
                                "option (default: 'BASENAME_heatmap.FORMAT')")
    output_options.add_argument("-x",metavar="XLSX",
                                dest="output_xlsx",
                                action="store",
                                default=None,
                                help="destination for output XLSX file "
                                "with the raw enrichment data (default: "
                                "'BASENAME_results.xlsx')")
    heatmap_options = p.add_argument_group("Heatmap options")
    heatmap_options.add_argument("--format",
                                 dest="heatmap_format",
                                 metavar="FORMAT",
                                 action="store",
                                 default = None,
                                 help="explicitly specify the image format "
                                 "for the output heatmap; note that if this "
                                 "option is specified then it will override "
                                 "the format implied by the specified with "
                                 "the -m option (default: 'png')")
    heatmap_options.add_argument("--x-label",
                                 metavar="CLUSTERS_AXIS_LABEL",
                                 dest="clusters_axis_label",
                                 action="store",
                                 default=None,
                                 help="set a custom label for the X "
                                 "(clusters) axis")
    heatmap_options.add_argument("--y-label",
                                 metavar="PEAKSETS_AXIS_LABEL",
                                 dest="peaksets_axis_label",
                                 action="store",
                                 default=None,
                                 help="set a custom label for the Y "
                                 "(peak sets) axis")
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
    # Deal with peak and cluster files
    peaks = sort_files(args.peaks)
    for f in peaks:
       if not os.path.exists(f):
          logging.fatal("Peaks file '%s' doesn't exist" % f)
          return 1
       elif os.path.isdir(f):
          logging.fatal("Peaks file '%s' is a directory (must be a file)"
                        % f)
          return 1
    clusters = sort_files(args.clusters)
    for f in clusters:
       if not os.path.exists(f):
          logging.fatal("Cluster file '%s' doesn't exist" % f)
          return 1
       elif os.path.isdir(f):
          logging.fatal("Cluster file '%s' is a directory (must be a file)"
                        % f)
          return 1
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
    # Check TADs file is actually a file
    if args.tads_file:
       if not os.path.exists(args.tads_file):
          logging.fatal("TADs file '%s' doesn't exist" % args.tads_file)
          return 1
       elif os.path.isdir(args.tads_file):
          logging.fatal("TADs file '%s' is a directory (must be a file)"
                        % args.tads_file)
          return 1
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
    print(PEGS_CITATION)

    print("====PEGS is starting====")

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
              peaks=peaks,
              clusters=clusters,
              tads_file=args.tads_file,
              name=args.name,
              heatmap=args.output_heatmap,
              xlsx=args.output_xlsx,
              output_directory=args.output_directory,
              keep_intersection_files=
              args.keep_intersection_files,
              clusters_axis_label=args.clusters_axis_label,
              peaksets_axis_label=args.peaksets_axis_label,
              heatmap_cmap=heatmap_cmap,
              heatmap_format=args.heatmap_format,
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
