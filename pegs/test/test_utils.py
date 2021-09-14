#!/usr/bin/env python

import unittest
import tempfile
import os
import shutil

from pegs.utils import find_exe
from pegs.utils import count_genes
from pegs.utils import collect_files
from pegs.utils import sort_files
from pegs.utils import split_file_name_for_sort
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
    def test_collect_files_for_clusters(self):
        """
        collect_files: returns list of cluster files in directory
        """
        cluster_files = [os.path.join(self.test_dir,
                                      "cluster_%s.txt" % name)
                         for name in ("1","2","3","10","null")]
        for f in cluster_files:
            with open(f,'wt') as fp:
                fp.write("4930516B21Rik\n")
        self.assertEqual(collect_files(self.test_dir),
                         cluster_files)

class TestSortFiles(unittest.TestCase):
    def test_sort_files(self):
        """
        sort_files: returns list of files sorted appropriately
        """
        self.assertEqual(sort_files(("file3","file1","file2")),
                         ["file1","file2","file3"])
        self.assertEqual(sort_files(("file10","file1","file21")),
                         ["file1","file10","file21"])
        self.assertEqual(sort_files(("file1_10","file1_1","file2_10")),
                         ["file1_1","file1_10","file2_10"])

class TestSplitFileNameForSort(unittest.TestCase):
    def test_split_file_name_for_sort(self):
        """
        split_file_name_for_sort: test names are split correctly
        """
        self.assertEqual(split_file_name_for_sort("peaks1.bed"),
                         ("peaks",1,".bed"))
        self.assertEqual(split_file_name_for_sort("cluster_10.txt"),
                         ("cluster_",10,".txt"))
        self.assertEqual(split_file_name_for_sort("cluster_10_0001.txt"),
                         ("cluster_",10,"_",1,".txt"))
        self.assertEqual(split_file_name_for_sort("cluster_10.0001.txt"),
                         ("cluster_",10,".",1,".txt"))

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
