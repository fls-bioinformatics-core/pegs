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

def get_cluster_files(d):
    """
    Collect cluster files from a directory

    Cluster files are expected to be named "cluster_<NAME>.txt"
    """
    cluster_files = filter(lambda f: fnmatch(basename(f),"cluster_*.txt"),
                           collect_files(abspath(d)))
    return sorted(cluster_files,
                  key=lambda f: get_cluster_name(f,as_padded_int=True))

def get_cluster_name(f,as_padded_int=False):
    """
    Return the cluster name from the file name

    Extracts the "<NAME>" component from files of the form
    "PATH/TO/cluster_<NAME>.txt"

    If the 'as_padded_int' argument is True then try to
    convert the name to an integer and return as a string
    padded with zeros (e.g. 12 -> "0000000012"), otherwise
    return it as a string.
    """
    name = basename(f)[8:-4]
    if as_padded_int:
        try:
            name = "%010d" % int(name)
        except ValueError:
            pass
    return name

def intersection_file_basename(interval_file,peak_file,distance=None):
    """
    Generate a name for an intersection file
    """
    return "%s.%s%s" % (splitext(basename(interval_file))[0],
                        splitext(basename(peak_file))[0],
                        (".%s" % distance if distance is not None else ""))
