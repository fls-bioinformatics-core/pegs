#!/usr/bin/env python

import unittest
import tempfile
import shutil
import os
import io
from pegs.intervals import make_gene_interval_file

class TestMakeGeneIntervalFile(unittest.TestCase):

    def setUp(self):
        # Store CWD
        self.cwd = os.getcwd()
        # Create test directory and move to it
        self.dirn = tempfile.mkdtemp(suffix='TestMakeGeneIntervalFile')
        os.chdir(self.dirn)

    def tearDown(self):
        # Return to CWD
        os.chdir(self.cwd)
        # Remove the temporary test directory
        shutil.rmtree(self.dirn)

    def test_make_gene_interval_file(self):
        """
        make_gene_interval_file: creates file of gene intervals
        """
        # Create test input
        test_input_file = os.path.join(self.dirn,"refGene.txt")
        with io.open(test_input_file,'wt') as fp:
            fp.write(u"""#bin	name	chrom	strand	txStart	txEnd	cdsStart	cdsEnd	exonCount	exonStarts	exonEnds	score	name2	cdsStartStat	cdsEndStat	exonFrames
0	NM_001291930	chr1	-	134199214	134235457	134202950	134203505	2	134199214,134235227,	134203590,134235457,	0	Adora1	cmpl	cmpl	0,-1,
0	NM_001291928	chr1	-	134199214	134234856	134202950	134234733	2	134199214,134234662,	134203590,134234856,	0	Adora1	cmpl	cmpl	2,0,
1	NM_008922	chr1	-	33453807	33669794	33454085	33669011	14	33453807,33464052,	33454304,33464121,	0	Prim2	cmpl	cmpl	0,0,
1	NM_001290392	chr1	-	8359738	9299877	8363474	8583258	18	8359738,8414202,	8363633,8414313,	0	Sntg1	cmpl	cmpl	0,0,
1	NM_175642	chr1	-	25067475	25829707	25068167	25826760	31	25067475,25074684,	25068356,25074789,	0	Adgrb3	cmpl	cmpl	0,0,
""")
        # Run the file generation
        make_gene_interval_file(test_input_file)
        # Check that the output file exists
        test_output_file =  os.path.join(self.dirn,"refGene_intervals.bed")
        self.assertTrue(os.path.exists(test_output_file))
        # Check the contents of the output file
        self.assertEqual(io.open(test_output_file,'rt').read(),
                         u"""chr1	25829707	25829708	Adgrb3
chr1	134235457	134235458	Adora1
chr1	33669794	33669795	Prim2
chr1	9299877	9299878	Sntg1
""")
