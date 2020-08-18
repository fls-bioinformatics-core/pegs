#!/usr/bin/env python
#
#     utils.py: utility functions for PEGS
#     Copyright (C) University of Manchester 2018-2020 Mudassar Iqbal, Peter Briggs
#

#######################################################################
# Imports
#######################################################################

import os
import io
from os import listdir
from os.path import isfile
from os.path import join
from os.path import abspath
from os.path import basename
from os.path import splitext
from fnmatch import fnmatch

#######################################################################
# Functions
#######################################################################

def find_exe(exe):
    """
    Locate an executable
    """
    if not os.path.isabs(exe):
        for p in os.environ['PATH'].split(os.pathsep):
            pth = join(p,exe)
            if isfile(pth) and os.access(pth,os.X_OK):
                return pth
    else:
        if os.path.isfile(exe) and os.access(exe,os.X_OK):
            return exe
    return None

def count_genes(bed_file):
    """
    Count the total number of genes in a BED file
    """
    print("Counting genes in %s" % basename(bed_file))
    m = 0
    with io.open(bed_file,'rt') as bed:
        for line in bed:
            m += 1
    print("Counted %d genes\n" % m)
    return m

def collect_files(d):
    """
    Collect files from a directory
    """
    return sorted([abspath(join(d,f))
                   for f in listdir(d) if isfile(join(d,f))])

def intersection_file_basename(interval_file,peak_file,distance=None):
    """
    Generate a name for an intersection file
    """
    return "%s.%s%s" % (splitext(basename(interval_file))[0],
                        splitext(basename(peak_file))[0],
                        (".%s" % distance if distance is not None else ""))
