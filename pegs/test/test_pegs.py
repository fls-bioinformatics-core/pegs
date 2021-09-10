#!/usr/bin/env python

import unittest
import tempfile
import os
import shutil
import numpy as np
import atexit

from pegs.pegs import make_expanded_bed
from pegs.pegs import get_overlapping_genes
from pegs.pegs import get_tads_overlapping_peaks
from pegs.pegs import calculate_enrichment
from pegs.pegs import calculate_enrichments
from pegs.pegs import pegs_main
from pegs.utils import find_exe
from pegs.bedtools import fetch_bedtools

# Module-level globals for managing bedtools install
BEDTOOLS_INSTALL_DIR = None
PATH_NO_BEDTOOLS = None
DESTROY_AT_EXIT = False

# Ensure that bedtools is available
def ensure_bedtools():
    # Globals
    global BEDTOOLS_INSTALL_DIR
    global PATH_NO_BEDTOOLS
    global DESTROY_AT_EXIT
    # Check if bedtools is already available
    if find_exe("bedtools"):
        return
    # Install bedtools in temp directory
    if BEDTOOLS_INSTALL_DIR is None:
        bedtools_install_dir = tempfile.mkdtemp()
        fetch_bedtools(install_dir=bedtools_install_dir,
                       create_install_dir=False)
        BEDTOOLS_INSTALL_DIR = bedtools_install_dir
        print("Installed bedtools in %s" % BEDTOOLS_INSTALL_DIR)
    # Append bedtools to the PATH
    if PATH_NO_BEDTOOLS is None:
        PATH_NO_BEDTOOLS = os.environ['PATH']
        os.environ['PATH'] = "%s%s%s" % (os.environ['PATH'],
                                         os.pathsep,
                                         BEDTOOLS_INSTALL_DIR)
    # Remove temporary bedtools install on exit
    if not DESTROY_AT_EXIT:
        atexit.register(remove_bedtools)
        DESTROY_AT_EXIT = True

# Restore the PATH to remove temporary bedtools
def restore_path():
    global PATH_NO_BEDTOOLS
    if PATH_NO_BEDTOOLS:
        os.environ['PATH'] = PATH_NO_BEDTOOLS
        PATH_NO_BEDTOOLS = None

# Remove the temporary bedtools install
def remove_bedtools():
    global BEDTOOLS_INSTALL_DIR
    if BEDTOOLS_INSTALL_DIR:
        try:
            print("Removing bedtools dir %s" % BEDTOOLS_INSTALL_DIR)
            shutil.rmtree(BEDTOOLS_INSTALL_DIR)
        except Exception:
            pass
        BEDTOOLS_INSTALL_DIR = None

class TestMakeExpandedBed(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    def test_make_expanded_bed(self):
        """
        make_expanded_bed: extend start and end in BED file
        """
        bed_file = os.path.join(self.test_dir,"in.bed")
        with open(bed_file,'wt') as fp:
            fp.write("""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""")
        expanded_file = os.path.join(self.test_dir,"out.bed")
        make_expanded_bed(bed_file,
                          expanded_file,
                          10000)
        expected_bed_data = """chr1	39746959	39767488
chr1	40268922	40289363
chr1	49022761	49043125
chr1	73352131	73372563
"""
        self.assertEqual(open(expanded_file,'rt').read(),
                         expected_bed_data)

class TestGetOverlappingGenes(unittest.TestCase):
    def setUp(self):
        ensure_bedtools()
        if not find_exe("bedtools"):
            self.skipTest("bedtools not found")
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        restore_path()
    def test_get_overlapping_genes(self):
        """
        get_overlapping_genes: returns set of gene names
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        peaks_file = os.path.join(self.test_dir,"peaks.bed")
        with open(peaks_file,'wt') as fp:
            fp.write("""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""")
        self.assertEqual(get_overlapping_genes(genes_file,
                                               peaks_file,
                                               interval=5000000,
                                               working_dir=self.test_dir),
                         set(("1500015O10Rik","Gm15179","Dnah7c")))
    def test_get_overlapping_genes_report_entire_feature(self):
        """
        get_overlapping_genes: returns set of gene names (report entire feature)
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        peaks_file = os.path.join(self.test_dir,"peaks.bed")
        with open(peaks_file,'wt') as fp:
            fp.write("""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""")
        self.assertEqual(get_overlapping_genes(genes_file,
                                               peaks_file,
                                               interval=5000000,
                                               report_entire_feature=True,
                                               working_dir=self.test_dir),
                         set(("1500015O10Rik","Gm15179","Dnah7c")))

class TestGetTadsOverlappingPeaks(unittest.TestCase):
    def setUp(self):
        ensure_bedtools()
        if not find_exe("bedtools"):
            self.skipTest("bedtools not found")
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        restore_path()
    def test_get_tads_overlapping_peaks(self):
        """
        get_tads_overlapping_peaks: return overlapping TADs
        """
        peaks_file = os.path.join(self.test_dir,"peaks.bed")
        with open(peaks_file,'wt') as fp:
            fp.write("""chr1	51097395	51097632
chr1	73090044	73090401
chr1	83125057	83125411
chr1	85758348	85758667
""")
        tads_file = os.path.join(self.test_dir,"tads.txt")
        with open(tads_file,'wt') as fp:
            fp.write("""chr1	23730601	26730602	TAD1
chr1	36425517	46425518	TAD2
chr1	75375015	85375016	TAD3
chr1	136212828	146212829	TAD4
""")
        tads_subset = os.path.join(self.test_dir,"tads_subset.bed")
        get_tads_overlapping_peaks(tads_file,peaks_file,tads_subset,
                                   working_dir=self.test_dir)
        expected_subset = """chr1	75375015	85375016	TAD3
"""
        with open(tads_subset,'rt') as fp:
            self.assertEqual(fp.read(),expected_subset)

class TestCalculateEnrichment(unittest.TestCase):
    def setUp(self):
        ensure_bedtools()
        if not find_exe("bedtools"):
            self.skipTest("bedtools not found")
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        restore_path()
    def test_calculate_enrichment(self):
        """
        calculate_enrichment: check calculated p-values and counts
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        ngenes = 5
        peaks_file = os.path.join(self.test_dir,"peaks.bed")
        with open(peaks_file,'wt') as fp:
            fp.write("""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""")
        cluster_dir = os.path.join(self.test_dir,"clusters")
        clusters = []
        os.mkdir(cluster_dir)
        for i,gene_cluster in enumerate((("1500015O10Rik",),
                                         ("Dnah7c","Gm15179",))):
            cluster_file = os.path.join(cluster_dir,
                                        "cluster_%d.txt" % i)
            with open(cluster_file,'wt') as fp:
                for gene in gene_cluster:
                    fp.write("%s\n" % gene)
            clusters.append(cluster_file)
        pvalues,counts = calculate_enrichment(genes_file,
                                              peaks_file,
                                              clusters,
                                              ngenes,
                                              self.test_dir,
                                              distance=5000000)
        expected_pvalues = np.array([0.6,0.3])
        expected_counts = np.array([1.0,2.0])
        # Use allclose to compare actual and expected
        # p-values (checks values are equal within a
        # tolerance)
        self.assertTrue(np.allclose(pvalues,expected_pvalues))
        # Use https://stackoverflow.com/q/3302949 to test
        # if actual and expected counts are exactly equal
        self.assertTrue((counts == expected_counts).all())

class TestCalculateEnrichments(unittest.TestCase):
    def setUp(self):
        ensure_bedtools()
        if not find_exe("bedtools"):
            self.skipTest("bedtools not found")
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        restore_path()
    def test_calculate_enrichments(self):
        """
        calculate_enrichments: check calculated p-values and counts
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        ngenes = 5
        peaks_data = (
"""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""",
"""chr1	51097395	51097632
chr1	73090044	73090401
chr1	83125057	83125411
chr1	85758348	85758667
""",
        )
        peaks = []
        for i,peakset in enumerate(peaks_data):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            with open(peaks_file,'wt') as fp:
                fp.write(peakset)
            peaks.append(peaks_file)
        cluster_dir = os.path.join(self.test_dir,"clusters")
        clusters = []
        os.mkdir(cluster_dir)
        for i,gene_cluster in enumerate((("1500015O10Rik",),
                                         ("Dnah7c","Gm15179",))):
            cluster_file = os.path.join(cluster_dir,
                                        "cluster_%d.txt" % i)
            with open(cluster_file,'wt') as fp:
                for gene in gene_cluster:
                    fp.write("%s\n" % gene)
            clusters.append(cluster_file)
        distances = [5000000,10000000]
        pvalues,counts,tads_pvalues,tads_counts = \
            calculate_enrichments(genes_file,
                                  distances,
                                  peaks,
                                  clusters,
                                  None)
        expected_pvalues = np.array([[[0.6,0.3],[0.6,0.3]],
                                     [[1.0,0.1],[0.6,0.3]]])
        expected_counts = np.array([[[1.0,2.0],[1.0,2.0]],
                                    [[0.0,2.0],[1.0,2.0]]])
        # Use allclose to compare actual and expected
        # p-values (checks values are equal within a
        # tolerance)
        self.assertTrue(np.allclose(pvalues,expected_pvalues))
        # Use https://stackoverflow.com/q/3302949 to test
        # if actual and expected counts are exactly equal
        self.assertTrue((counts == expected_counts).all())
        # No TADs
        self.assertEqual(tads_pvalues,None)
        self.assertEqual(tads_counts,None)
    def test_calculate_enrichments_with_tads(self):
        """
        calculate_enrichments: include TADs
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        ngenes = 5
        peaks_data = (
"""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""",
"""chr1	51097395	51097632
chr1	73090044	73090401
chr1	83125057	83125411
chr1	85758348	85758667
""",
        )
        peaks = []
        for i,peakset in enumerate(peaks_data):
            peaks_file = os.path.join(self.test_dir,
                                      "peaks%d.bed" % i)
            with open(peaks_file,'wt') as fp:
                fp.write(peakset)
            peaks.append(peaks_file)
        cluster_dir = os.path.join(self.test_dir,"clusters")
        clusters = []
        os.mkdir(cluster_dir)
        for i,gene_cluster in enumerate((("1500015O10Rik",),
                                         ("Dnah7c","Gm15179",))):
            cluster_file = os.path.join(cluster_dir,
                                        "cluster_%d.txt" % i)
            with open(cluster_file,'wt') as fp:
                for gene in gene_cluster:
                    fp.write("%s\n" % gene)
            clusters.append(cluster_file)
        tads_file = os.path.join(self.test_dir,"tads.txt")
        with open(tads_file,'wt') as fp:
            fp.write("""chr1	23730601	26730602	TAD1
chr1	36425517	46425518	TAD2
chr1	75375015	85375016	TAD3
chr1	136212828	146212829	TAD4
""")
        distances = [5000000,10000000]
        pvalues,counts,tads_pvalues,tads_counts = \
            calculate_enrichments(genes_file,
                                  distances,
                                  peaks,
                                  clusters,
                                  tads_file)
        expected_pvalues = np.array([[[0.6,0.3],[0.6,0.3]],
                                     [[1.0,0.1],[0.6,0.3]]])
        expected_counts = np.array([[[1.0,2.0],[1.0,2.0]],
                                    [[0.0,2.0],[1.0,2.0]]])
        expected_pvalues_tads = np.array([[0.4,0.7],
                                          [1.0,0.4]])
        expected_counts_tads = np.array([[1.0,1.0],
                                          [0.0,1.0]])
        # Use allclose to compare actual and expected
        # p-values (checks values are equal within a
        # tolerance)
        self.assertTrue(np.allclose(pvalues,expected_pvalues))
        self.assertTrue(np.allclose(tads_pvalues,expected_pvalues_tads))
        # Use https://stackoverflow.com/q/3302949 to test
        # if actual and expected counts are exactly equal
        self.assertTrue((counts == expected_counts).all())
        self.assertTrue((tads_counts == expected_counts_tads).all())

class TestPegsMain(unittest.TestCase):
    def setUp(self):
        ensure_bedtools()
        if not find_exe("bedtools"):
            self.skipTest("bedtools not found")
        self.test_dir = tempfile.mkdtemp()
    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
        restore_path()
    def test_pegs_main(self):
        """
        pegs_main: generates heatmap and XLSX files
        """
        genes_file = os.path.join(self.test_dir,"genes.bed")
        with open(genes_file,'wt') as fp:
            fp.write("""chr1	9547947	9547948	Adhfe1
chr1	43730601	43730602	1500015O10Rik
chr1	46425517	46425518	Dnah7c
chr1	75375015	75375016	Gm15179
chr1	136212828	136212829	Mroh3
""")
        ngenes = 5
        peaks_data = (
"""chr1	39756959	39757488
chr1	40278922	40279363
chr1	49032761	49033125
chr1	73362131	73362563
""",
"""chr1	51097395	51097632
chr1	73090044	73090401
chr1	83125057	83125411
chr1	85758348	85758667
""",
        )
        peaks = []
        peaks_dir = os.path.join(self.test_dir,"peaks")
        os.mkdir(peaks_dir)
        for i,peakset in enumerate(peaks_data):
            peaks_file = os.path.join(peaks_dir,
                                      "peaks%d.bed" % i)
            with open(peaks_file,'wt') as fp:
                fp.write(peakset)
            peaks.append(peaks_file)
        cluster_dir = os.path.join(self.test_dir,"clusters")
        clusters = []
        os.mkdir(cluster_dir)
        for i,gene_cluster in enumerate((("1500015O10Rik",),
                                         ("Dnah7c","Gm15179",))):
            cluster_file = os.path.join(cluster_dir,
                                        "cluster_%d.txt" % i)
            with open(cluster_file,'wt') as fp:
                for gene in gene_cluster:
                    fp.write("%s\n" % gene)
            clusters.append(cluster_file)
        tads_file = os.path.join(self.test_dir,"tads.txt")
        with open(tads_file,'wt') as fp:
            fp.write("""chr1	23730601	26730602	TAD1
chr1	36425517	46425518	TAD2
chr1	75375015	85375016	TAD3
chr1	136212828	146212829	TAD4
""")
        distances = [5000000,10000000]
        pegs_main(genes_file,
                  distances,
                  peaks,
                  clusters,
                  tads_file,
                  "pegs_test",
                  output_directory=self.test_dir)
        # Check output files exist
        self.assertTrue(os.path.exists(
            os.path.join(self.test_dir,"pegs_test_heatmap.png")
        ))
        self.assertTrue(os.path.exists(
            os.path.join(self.test_dir,"pegs_test_results.xlsx")
        ))
