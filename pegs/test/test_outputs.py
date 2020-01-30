#!/usr/bin/env python

import unittest
import tempfile
import os
import shutil
import numpy as np

from pegs.outputs import make_heatmap
from pegs.outputs import make_xlsx_file

class TestMakeHeatmap(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_make_heatmap(self):
        """
        make_heatmap: generates heatmap PNG
        """
        peaks = []
        for i in range(2):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            peaks.append(peaks_file)
        clusters = []
        for i in range(2):
            cluster_file = os.path.join(self.test_dir,
                                        "cluster_%d.txt" % i)
            clusters.append(cluster_file)
        distances = [5000000,10000000]
        pvalues = np.array([[[0.9,0.3],[0.9,0.3]],
                            [[1.0,0.1],[0.9,0.3]]])
        counts = np.array([[[1.0,2.0],[1.0,2.0]],
                           [[0.0,2.0],[1.0,2.0]]])
        heatmap_file = os.path.join(self.test_dir,
                                    "pegs_test_heatmap.png")
        make_heatmap(heatmap_file,
                     peaks,clusters,distances,
                     pvalues,counts)
        self.assertTrue(os.path.exists(heatmap_file))
    def test_make_heatmap_with_tads(self):
        """
        make_heatmap: generates heatmap PNG including TADs data
        """
        peaks = []
        for i in range(2):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            peaks.append(peaks_file)
        clusters = []
        for i in range(2):
            cluster_file = os.path.join(self.test_dir,
                                        "cluster_%d.txt" % i)
            clusters.append(cluster_file)
        distances = [5000000,10000000]
        pvalues = np.array([[[0.9,0.3],[0.9,0.3]],
                            [[1.0,0.1],[0.9,0.3]]])
        counts = np.array([[[1.0,2.0],[1.0,2.0]],
                           [[0.0,2.0],[1.0,2.0]]])
        pvalues_tads = np.array([[0.7,0.7],[1.0,0.4]])
        counts_tads = np.array([[1.0,1.0],[0.0,1.0]])
        heatmap_file = os.path.join(self.test_dir,
                                    "pegs_test_heatmap.png")
        make_heatmap(heatmap_file,
                     peaks,clusters,distances,
                     pvalues,counts,
                     tads_pvalues=pvalues_tads,
                     tads_counts=counts_tads)
        self.assertTrue(os.path.exists(heatmap_file))

class TestMakeXlsxFile(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_make_xlsx_file(self):
        """
        make_xlsx_file: generates XLSX file
        """
        peaks = []
        for i in range(2):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            peaks.append(peaks_file)
        clusters = []
        for i in range(2):
            cluster_file = os.path.join(self.test_dir,
                                        "cluster_%d.txt" % i)
            clusters.append(cluster_file)
        distances = [5000000,10000000]
        pvalues = np.array([[[0.9,0.3],[0.9,0.3]],
                            [[1.0,0.1],[0.9,0.3]]])
        counts = np.array([[[1.0,2.0],[1.0,2.0]],
                           [[0.0,2.0],[1.0,2.0]]])
        xlsx_file = os.path.join(self.test_dir,
                                 "pegs_test_result.xlsx")
        make_xlsx_file(xlsx_file,
                       peaks,clusters,distances,
                       pvalues,counts)
        self.assertTrue(os.path.exists(xlsx_file))
    def test_make_xlsx_file_with_tads(self):
        """
        make_xlsx_file: generates XLSX file including TADs data
        """
        peaks = []
        for i in range(2):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            peaks.append(peaks_file)
        clusters = []
        for i in range(2):
            cluster_file = os.path.join(self.test_dir,
                                        "cluster_%d.txt" % i)
            clusters.append(cluster_file)
        distances = [5000000,10000000]
        pvalues = np.array([[[0.9,0.3],[0.9,0.3]],
                            [[1.0,0.1],[0.9,0.3]]])
        counts = np.array([[[1.0,2.0],[1.0,2.0]],
                           [[0.0,2.0],[1.0,2.0]]])
        pvalues_tads = np.array([[0.7,0.7],[1.0,0.4]])
        counts_tads = np.array([[1.0,1.0],[0.0,1.0]])
        xlsx_file = os.path.join(self.test_dir,
                                 "pegs_test_result.xlsx")
        make_xlsx_file(xlsx_file,
                       peaks,clusters,distances,
                       pvalues,counts,
                       tads_pvalues=pvalues_tads,
                       tads_counts=counts_tads)
        self.assertTrue(os.path.exists(xlsx_file))

        
