#!/usr/bin/env python

import unittest
import tempfile
import os
import shutil

from pegs.utils import find_exe
from pegs.utils import count_genes
from pegs.utils import collect_files
from pegs.utils import get_cluster_files
from pegs.utils import get_cluster_name
from pegs.utils import intersection_file_basename

class TestFindExe(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_find_exe_on_path(self):
        """
        find_exe: locates executable file on PATH
        """
        full_path = os.path.join(self.test_dir,"test.exe")
        with open(full_path,'wt') as fp:
            fp.write("#!/usr/bin/bash\necho Test")
        os.chmod(full_path,0o755)
        os.environ['PATH'] = "%s%s%s" % (os.environ['PATH'],
                                         os.pathsep,
                                         self.test_dir)
        self.assertEqual(find_exe(os.path.basename(full_path)),
                         full_path)
    def test_find_exe_full_path(self):
        """
        find_exe: locates executable file given full path
        """
        full_path = os.path.join(self.test_dir,"test.exe")
        with open(full_path,'wt') as fp:
            fp.write("#!/usr/bin/bash\necho Test")
        os.chmod(full_path,0o755)
        self.assertEqual(find_exe(full_path),full_path)
    def test_find_exe_for_missing_file(self):
        """
        find_exe: returns None if file not found
        """
        self.assertEqual(find_exe("doesntexist"),None)
        self.assertEqual(find_exe("/no/where/doesntexist"),None)

class TestCountGenes(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_count_genes(self):
        """
        count_genes: get number of genes in file
        """
        bed_file = os.path.join(self.test_dir,"genes.bed")
        with open(bed_file,'wt') as fp:
            fp.write("""chr3	67892219	67892220	Iqcj
chr12	81568474	81568475	Adam21
chr9	56418050	56418051	Peak1
chr11	49663594	49663595	Scgb3a1
""")
        self.assertEqual(count_genes(bed_file),4)

class TestCollectFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_collect_files(self):
        """
        collect_files: returns list of files in directory
        """
        files = [os.path.join(self.test_dir,f)
                 for f in ("file1","file2","file3")]
        for f in files:
            with open(f,'wt') as fp:
                fp.write("test\n")
        self.assertEqual(collect_files(self.test_dir),
                         files)

class TestGetClusterFiles(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_get_cluster_files(self):
        """
        get_cluster_files: returns "cluster_*.txt" files from directory
        """
        cluster_files = [os.path.join(self.test_dir,
                                      "cluster_%s.txt" % name)
                         for name in ("1","2","3","10","null")]
        for f in cluster_files:
            with open(f,'wt') as fp:
                fp.write("4930516B21Rik\n")
        extra_files = [os.path.join(self.test_dir,f)
                       for f in ("cluster_1.bed","other.txt")]
        self.assertEqual(get_cluster_files(self.test_dir),
                         cluster_files)

class TestGetClusterName(unittest.TestCase):
    def test_get_cluster_name(self):
        """
        get_cluster_name: extract cluster name from file path
        """
        self.assertEqual(get_cluster_name("/path/to/cluster_1.txt"),"1")
        self.assertEqual(get_cluster_name("/path/to/cluster_10.txt"),"10")
        self.assertEqual(get_cluster_name("/path/to/cluster_null.txt"),"null")
    def test_get_cluster_name_as_padded_integer(self):
        """
        get_cluster_name: extract cluster name and convert to padded integer
        """
        self.assertEqual(get_cluster_name("/path/to/cluster_1.txt",
                                          as_padded_int=True),
                         "0000000001")
        self.assertEqual(get_cluster_name("/path/to/cluster_10.txt",
                                          as_padded_int=True),
                         "0000000010")
        self.assertEqual(get_cluster_name("/path/to/cluster_null.txt",
                                          as_padded_int=True),
                         "null")

class TestIntersectionFileBasename(unittest.TestCase):
    def test_intersection_file_basename(self):
        """
        intersection_file_basename: generates basename
        """
        self.assertEqual(
            intersection_file_basename(
                "/data/mm10/refGene_mm10.bed",
                "/data/peaks/Peaks-E1234-merged.bed",
                5000),
            "refGene_mm10.Peaks-E1234-merged.5000")
    def test_intersection_file_basename_no_distance(self):
        """
        intersection_file_basename: no distance supplied
        """
        self.assertEqual(
            intersection_file_basename(
                "/data/mm10/refGene_mm10.bed",
                "/data/peaks/Peaks-E1234-merged.bed"),
            "refGene_mm10.Peaks-E1234-merged")
    def test_intersection_file_basename_distance_is_None(self):
        """
        intersection_file_basename: distance is 'None'
        """
        self.assertEqual(
            intersection_file_basename(
                "/data/mm10/refGene_mm10.bed",
                "/data/peaks/Peaks-E1234-merged.bed",
                None),
            "refGene_mm10.Peaks-E1234-merged")
