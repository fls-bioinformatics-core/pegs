#!/usr/bin/env python
#
#     bedtools.py: utility functions for bedtools in PEGS
#     Copyright (C) University of Manchester 2020-2021 Mudassar Iqbal, Peter Briggs
#

#######################################################################
# Imports
#######################################################################

import os
import io
import shutil
from urllib.request import urlopen
from urllib.error import URLError
import tempfile
import subprocess
import logging

#######################################################################
# Functions
#######################################################################

def intersect(infile_a,infile_b,outfile,working_dir=None,
              report_entire_feature=False,bedtools_exe="bedtools"):
    """
    Run 'bedtools intersect'

    infile_a (str): path to input file 'A' (-a)
    infile_b (str): path to input file 'B' (-b)
    outfile (str): path to output file
    working_dir (str): (optional) working directory to run
      'intersectBed' in (defaults to CWD)
    report_entire_feature (bool): (optional) if True then
      write the original entry in 'A' for each overlap (-wa)
    bedtools_exe (str): 'bedtools' executable to use

    Returns the name of the output file.
    """
    # Working directory
    if working_dir is None:
        wd = os.getcwd()
    else:
        wd = os.path.abspath(working_dir)
    # Build command
    cmd = [bedtools_exe,"intersect"]
    if report_entire_feature:
        cmd.append("-wa")
    cmd.extend(["-a",infile_a,
                "-b",infile_b])
    # Run command
    with io.open(outfile,'wt') as output:
        exit_code = subprocess.call(cmd,cwd=wd,stdout=output)
    return outfile

def bedtools_version(bedtools_exe="bedtools"):
    """
    Returns the version number for bedtools
    """
    bedtools_version = subprocess.check_output([bedtools_exe,
                                                '--version'])
    return bedtools_version.decode().strip()

def fetch_bedtools(install_dir,create_install_dir=False):
    """
    Attempt to download bedtools

    By default tries to download 'bedtools' and install into the
    specified directory.

    The installation directory must already exist, unless
    'create_install_dir' is set (in which case the installation
    directory will be created first).

    Returns the location for the acquired bedtools executable
    """
    # Check the installation directory
    install_dir = os.path.abspath(install_dir)
    if not os.path.exists(install_dir):
        if create_install_dir:
            print("...creating installation directory '%s'" % install_dir)
            try:
                os.makedirs(install_dir)
            except Exception as ex:
                logging.error("Couldn't make installation directory "
                              "for 'bedtools': %s" % ex)
                return None
        else:
            logging.error("Installation directory '%s' not found" %
                          install_dir)
            return None
    # Download bedtools to temporary area
    download_url = "https://github.com/arq5x/bedtools2/releases/download/v2.29.2/bedtools.static.binary"
    print("...downloading 'bedtools' from %s" % download_url)
    download_dir = tempfile.mkdtemp()
    tmp_bedtools = os.path.join(download_dir,"bedtools")
    try:
        urlfp = urlopen(download_url)
        with open(tmp_bedtools,'wb') as fp:
            fp.write(urlfp.read())
        os.chmod(tmp_bedtools,0o755)
    except Exception as ex:
        # Failed to download from URL
        logging.error("Couldn't fetch 'bedtools' from '%s': %s" %
                      (download_url,ex))
        return None
    # Install bedtools
    print("...installing 'bedtools' into %s" % install_dir)
    try:
        # Use copy/remove instead of os.rename as latter can't
        # move files across different devices
        shutil.copy(tmp_bedtools,os.path.join(install_dir,"bedtools"))
        os.remove(tmp_bedtools)
    except Exception as ex:
        # Failed to move to installation directory
        logging.error("Couldn't move 'bedtools' to '%s': %s" %
                      (install_dir,ex))
        return None
    return os.path.join(install_dir,"bedtools")
