#!/usr/bin/env python

import unittest
import tempfile
import os
import shutil

from pegs.bedtools import intersect
from pegs.bedtools import bedtools_version
from pegs.bedtools import fetch_bedtools

class TestIntersect(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def _make_bedtools_exe(self):
        self.bedtools_exe = os.path.join(self.test_dir,"bedtools")
        with open(self.bedtools_exe,'wt') as fp:
            fp.write("""#!/usr/bin/env python
import os
from argparse import ArgumentParser
p = ArgumentParser()
s = p.add_subparsers()
intersect = s.add_parser("intersect")
intersect.add_argument("-wa",action='store_true')
intersect.add_argument("-a",action='store')
intersect.add_argument("-b",action='store')
args = p.parse_args()
print("CWD:%s" % os.getcwd())
print("a:%s" % args.a)
print("b:%s" % args.b)
print("wa:%s" % args.wa)
""")
        os.chmod(self.bedtools_exe,0o755)
    def test_intersect(self):
        """
        intersect: run 'bedtools intersect'
        """
        self._make_bedtools_exe()
        outfile = os.path.join(self.test_dir,"out.txt")
        outfile2 = intersect("/data/infile_a",
                           "/data/infile_b",
                           outfile,
                           working_dir=self.test_dir,
                           report_entire_feature=False,
                           bedtools_exe=self.bedtools_exe)
        self.assertEqual(outfile2,outfile)
        self.assertTrue(os.path.exists(outfile))
        with open(outfile,'rt') as fp:
            for line in fp.read().strip().split('\n'):
                key,value = line.split(':')
                if key == "CWD":
                    self.assertEqual(value,self.test_dir)
                elif key == "a":
                    self.assertEqual(value,"/data/infile_a")
                elif key == "b":
                    self.assertEqual(value,"/data/infile_b")
                elif key == "wa":
                    self.assertEqual(value,"False")
                else:
                    self.fail("Bad output")
    def test_intersect_report_entire_feature(self):
        """
        intersect: run 'bedtools intersect' (report entire feature)
        """
        self._make_bedtools_exe()
        outfile = os.path.join(self.test_dir,"out.txt")
        outfile2 = intersect("/data/infile_a",
                           "/data/infile_b",
                           outfile,
                           working_dir=self.test_dir,
                           report_entire_feature=True,
                           bedtools_exe=self.bedtools_exe)
        self.assertEqual(outfile2,outfile)
        self.assertTrue(os.path.exists(outfile))
        with open(outfile,'rt') as fp:
            for line in fp.read().strip().split('\n'):
                key,value = line.split(':')
                if key == "CWD":
                    self.assertEqual(value,self.test_dir)
                elif key == "a":
                    self.assertEqual(value,"/data/infile_a")
                elif key == "b":
                    self.assertEqual(value,"/data/infile_b")
                elif key == "wa":
                    self.assertEqual(value,"True")
                else:
                    self.fail("Bad output")

class TestBedtoolsVersion(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def _make_bedtools_exe(self):
        self.bedtools_exe = os.path.join(self.test_dir,"bedtools")
        with open(self.bedtools_exe,'wt') as fp:
            fp.write("""#!/usr/bin/env python
import os
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--version',action='store_true')
args = p.parse_args()
if args.version:
    print("bedtools v1.2.3")
""")
        os.chmod(self.bedtools_exe,0o755)
    def test_bedtools_version(self):
        """
        bedtools_version: get version from 'bedtools'
        """
        self._make_bedtools_exe()
        self.assertEqual(bedtools_version(bedtools_exe=self.bedtools_exe),
                         "bedtools v1.2.3")

class TestFetchBedtools(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_fetch_bedtools(self):
        """
        fetch_bedtools: install to existing directory
        """
        # Make an installation directory
        install_dir = os.path.join(self.test_dir,"bin")
        os.mkdir(install_dir)
        self.assertEqual(fetch_bedtools(install_dir),
                         os.path.join(install_dir,"bedtools"))
        self.assertTrue(os.path.exists(os.path.join(install_dir,
                                                    "bedtools")))
    def test_fetch_bedtools_missing_install_dir(self):
        """
        fetch_bedtools: fails by default for missing install directory
        """
        install_dir = os.path.join(self.test_dir,"bin")
        self.assertFalse(os.path.exists(install_dir))
        self.assertEqual(fetch_bedtools(install_dir),None)
        self.assertFalse(os.path.exists(os.path.join(install_dir,
                                                    "bedtools")))
    def test_fetch_bedtools_create_install_dir(self):
        """
        fetch_bedtools: create directory before installation
        """
        install_dir = os.path.join(self.test_dir,"bin")
        self.assertFalse(os.path.exists(install_dir))
        self.assertEqual(fetch_bedtools(install_dir,
                                        create_install_dir=True),
                         os.path.join(install_dir,"bedtools"))
        self.assertTrue(os.path.exists(install_dir))
        self.assertTrue(os.path.exists(os.path.join(install_dir,
                                                    "bedtools")))
