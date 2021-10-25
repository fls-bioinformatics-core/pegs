#!/usr/bin/env python
#
#     utils.py: utility functions for PEGS
#     Copyright (C) University of Manchester 2018-2021 Mudassar Iqbal, Peter Briggs
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
# Classes
#######################################################################

class SortableFilename:
    """
    Utility class for sorting file names
    """
    def __init__(self,f):
        """
        Arguments:
          f (str): the file name to sort on
        """
        self.components = split_file_name_for_sort(os.path.basename(f))
    def __lt__(self,other):
        """
        Implement the __lt__ (less than) built-in method
        """
        for s,o in zip(self.components,other.components):
            try:
                if s < o:
                    return True
            except TypeError:
                if str(s) < str(o):
                    return True
        return False

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
    return sort_files([abspath(join(d,f))
                       for f in listdir(d) if isfile(join(d,f))
                       and not f.startswith('.')
                       and not f.endswith('~')])

def sort_files(f):
    """
    Sort files based on integer components
    """
    return sorted(f,key=SortableFilename)

def split_file_name_for_sort(f):
    """
    Returns tuple of string and integer components for sorting

    For example:

    "cluster_10.txt" -> ("cluster_",10,".txt")
    """
    components = []
    current_component = ''
    component_is_digits = False
    # Loop over characters in the input string
    for c in str(f):
        if current_component:
            # Already building a group of characters
            if (c.isdigit() and not component_is_digits) or \
               (not c.isdigit() and component_is_digits):
                # Next character is a different type from
                # the current group, so the current group
                # is complete
                if component_is_digits:
                    # Convert digits to integer
                    current_component = int(current_component)
                components.append(current_component)
                # Reset for a new group of characters
                current_component = ''
                component_is_digits = False
            else:
                # Next character is same type as current
                # group, just append it
                current_component += c
        if not current_component:
            # Next character starts a new group
            current_component += c
            component_is_digits = c.isdigit()
    # Finished looping, check if there is a final
    # unprocessed character group
    if current_component:
        if component_is_digits:
            # Convert digits to integer
            current_component = int(current_component)
        components.append(current_component)
    # Return the tuple of elements
    return tuple(components)

def intersection_file_basename(interval_file,peak_file,distance=None):
    """
    Generate a name for an intersection file
    """
    return "%s.%s%s" % (splitext(basename(interval_file))[0],
                        splitext(basename(peak_file))[0],
                        (".%s" % distance if distance is not None else ""))
