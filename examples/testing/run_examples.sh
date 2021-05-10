#!/bin/bash
#
# Run examples for PEGS
#
# Executables
PEGS="${PEGS:-pegs}"
MK_PEGS_INTERVALS="$(dirname $(which $PEGS))/mk_pegs_intervals"
#
# Assertion functions for tests
_PASSED=0
_FAILED=0
_SKIPPED=0
report_tests() {
    # Report summary of tests passed and failed
    local n_tests=$((_PASSED+_FAILED))
    echo "---------------------------------------------------------"
    echo -n "Ran $n_tests tests"
    if [ $_SKIPPED -ne 0 ] ; then
	echo -n " (skipped $_SKIPPED)"
    fi
    echo ": $_PASSED passed, $_FAILED failed"
    if [ $_FAILED -ne 0 ] ; then
	return 1
    else
	return 0
    fi
}
run_test() {
    # Run a command and check outputs
    # Takes following arguments:
    # --command CMD: specify the command to execute
    # --expected FILES: list of file names which should
    #                have reference versions to compare
    #                against
    # --must_exist FILES: list of file names which should
    #                exist after the command has run
    # --status INT: exit code to check (if command was
    #                run externally)
    # --strip-paths: strip leading paths found inside
    #                reference and output files when
    #                checking content matches
    # --rename OLD NEW: rename file OLD to NEW before
    #                checking
    # --skip:        don't run the test
    local test_name="$1"
    local command=
    local expected_outputs=
    local check_exists=
    local exit_status=
    local working_dir=
    local test_status=
    local strip_paths=
    local rename_files=
    local skip=
    # Collect arguments
    shift
    while [ $# -gt 0 ] ; do
	case $1 in
	    --command)
		command=$2
		shift
		;;
	    --expected)
		expected_outputs=$2
		shift
		;;
	    --must_exist)
		check_exists=$2
		shift
		;;
	    --status)
		exit_status=$2
		shift
		;;
	    --strip-paths)
		strip_paths=$1
		;;
	    --rename)
		rename_files="$rename_files $2 $3"
		shift ; shift
		;;
	    --skip)
		skip=$1
		;;
	    *)
		echo "$test_name: SKIPPED (unrecognised test argument '$1')"
		return
		;;
	esac
	shift
    done
    echo "---------------------------------------------------------"
    echo test_name: $test_name
    echo command: $command
    echo expected_outputs: $expected_outputs
    echo check_exists: $check_exists
    echo exit_status: $exit_status
    echo strip_paths: $strip_paths
    echo rename: $rename_files
    echo skip: $skip
    echo PWD: $(pwd)
    # Skip the test
    if [ ! -z "$skip" ] ; then
	command=
	exit_status=
	rename_files=
	expected_outputs=
	check_exists=
	test_status=SKIPPED
    fi
    # If command supplied then run it
    if [ ! -z "$command" ] ; then
	working_dir=$(mktemp -d --tmpdir=$(pwd))
	echo working_dir: $working_dir
	cd $working_dir
	echo "Running command"
	$command 1>STDOUT 2>STDERR
	exit_status=$?
	echo "Exit status $exit_status"
    fi
    # Check exit status
    if [ ! -z "$exit_status" ] ; then
	if [ $exit_status -ne 0 ] ; then
	    echo Failed exit status check
	    test_status=FAILED
	fi
    fi
    # Rename files
    if [ ! -z "$rename_files" ] ; then
	old=
	for f in $rename_files ; do
	    if [ -z "$old" ] ; then
		old=$f
	    else
		if [ ! -f $old ] ; then
                    echo "$f: missing"
		    echo Failed rename operation
		    test_status=FAILED
		else
		    /bin/mv -f $old $f
		fi
		old=
	    fi
	done
    fi
    # Compare expected outputs
    for f in $expected_outputs ; do
	assert_equal $REF_DATA/ref_$f $f $strip_paths
	if [ $? -ne 0 ] ; then
	    echo Failed output comparison check
	    test_status=FAILED
	fi
    done
    # Check existence
    for f in $check_exists ; do
	if [ ! -e $f ] ; then
	    echo "$f: missing"
	    echo Failed output existence check
	    test_status=FAILED
	fi
    done
    # Set test status if no failures
    if [ -z "$test_status" ] ; then
	test_status=OK
    fi
    echo test_status: $test_status
    # Report logs from failed job
    if [ $test_status = FAILED ] ; then
	for f in STDOUT STDERR ; do
	    if [ -e $f ] ; then
		echo "===== $test_name: $f ====="
		cat $f
	    fi
	done
    fi
    # Clean up any working area
    if [ ! -z "$working_dir" ] ; then
	cd ..
	#rm -rf $working_dir
    fi
    # Test counts
    case $test_status in
	OK)
	    _PASSED=$((_PASSED+1))
	    ;;
	FAILED)
	    _FAILED=$((_FAILED+1))
	    ;;
	SKIPPED)
	    _SKIPPED=$((_SKIPPED+1))
    esac
    # Finish
    echo "---------------------------------------------------------"
    echo "TEST: $test_name: $test_status"
}
assert_equal() {
    # Check two files are the same
    local strip_paths=
    if [ "$3" = "--strip-paths" ] ; then
	strip_paths=yes
    fi
    if [ ! -e $1 ] ; then
	echo "$1: missing reference data"
	return 1
    elif [ ! -e $2 ] ; then
	echo "$2: missing"
	return 1
    fi
    if [ -z "$strip_paths" ] ; then
	old=$1
	new=$2
    else
	tmpdir=$(mktemp -d)
	old=$tmpdir/old
	sed 's,/.*/,,g' $1 >$old
	new=$tmpdir/new
	sed 's,/.*/,,g' $2 >$new
    fi
    diff -q $old $new
    if [ $? -ne 0 ] ; then
	echo "$2: doesn't match reference data:"
	diff $1 $2
	return 1
    else
	return 0
    fi
}
#
# Initialise and set up dir for test outputs
TEST_DIR=$(dirname $0)
if [ "$TEST_DIR" = "." ] ; then
    TEST_DIR=$(pwd)
elif [ -z "$(echo $TEST_DIR | grep ^/)" ] ; then
    TEST_DIR=$(pwd)/$TEST_DIR
fi
DATA_DIR=$TEST_DIR/test-data
REF_DATA=$TEST_DIR/ref-data
if [ ! -d test-output ] ; then
    mkdir test-output
else
    rm -rf test-output/*
fi
cd test-output
#
# pegs with initial test data
run_test "pegs: initial test data" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --expected "pegs_count.tsv pegs_pval.tsv" \
    --command "pegs $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters --dump-raw-data"
#
# pegs with TADS
run_test "pegs: initial test data with TADS" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --expected "pegs_count.tsv pegs_tads_count.tsv pegs_pval.tsv pegs_tads_pval.tsv" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters -t $DATA_DIR/tads.txt --dump-raw-data"
#
# pegs with built-in gene intervals
run_test "pegs: using built-in mm10 data" \
    --rename pegs_count.tsv pegs_mm10_builtin_count.tsv \
    --rename pegs_pval.tsv pegs_mm10_builtin_pval.tsv \
    --expected "pegs_mm10_builtin_count.tsv pegs_mm10_builtin_pval.tsv" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --command "$PEGS mm10 $DATA_DIR/peaksets $DATA_DIR/clusters --dump-raw-data"
#
# pegs keeping intermediate intersection files
run_test "pegs: keep intersection files" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx
    intersection_beds/Intersection.gene_intervals.peakset1.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset2.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset3.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset1.25000.bed
    intersection_beds/Intersection.gene_intervals.peakset2.25000.bed
    intersection_beds/Intersection.gene_intervals.peakset3.25000.bed" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters 5000,25000 --keep-intersection-files"
#
# pegs keeping intermediate intersection files (including TADS)
run_test "pegs: keep intersection files (including TADS)" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx
    intersection_beds/Intersection.gene_intervals.peakset1.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset2.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset3.5000.bed
    intersection_beds/Intersection.gene_intervals.peakset1.25000.bed
    intersection_beds/Intersection.gene_intervals.peakset2.25000.bed
    intersection_beds/Intersection.gene_intervals.peakset3.25000.bed
    intersection_beds/Intersection.gene_intervals.peakset1.tads.bed
    intersection_beds/Intersection.gene_intervals.peakset2.tads.bed
    intersection_beds/Intersection.gene_intervals.peakset3.tads.bed" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters 5000,25000 -t $DATA_DIR/tads.txt --keep-intersection-files"
#
# pegs with --name option
run_test "pegs: specify basename for output files" \
    --must_exist "test_heatmap.png test_results.xlsx test_count.tsv test_pval.tsv" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters --dump-raw-data --name test"
#
# pegs with TADS and --name option
run_test "pegs: specify basename for output files (with TADS)" \
    --must_exist "test_heatmap.png test_results.xlsx test_count.tsv test_tads_count.tsv test_pval.tsv test_tads_pval.tsv" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters -t $DATA_DIR/tads.txt --dump-raw-data --name test"
#
# pegs specifying distances as multiple values
run_test "pegs: specify distances as multiple values" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --expected "pegs_count.tsv pegs_pval.tsv" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters 5000 25000 50000 100000 150000 200000 --dump-raw-data"
#
# pegs specifying distances as single comma-separated argument
run_test "pegs: specify distances as single comma-separated argument" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --expected "pegs_count.tsv pegs_pval.tsv" \
    --command "$PEGS --dump-raw-data $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters 5000,25000,50000,100000,150000,200000"
#
# pegs specifying custom heatmap palette settings
run_test "pegs: customise heatmap palette options" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters --heatmap-palette start=2 reverse=True"
#
# pegs specifying custom color scheme for heatmap
run_test "pegs: specify alternative colour scheme for heatmap" \
    --must_exist "pegs_heatmap.png pegs_results.xlsx" \
    --command "$PEGS $DATA_DIR/gene_intervals.bed $DATA_DIR/peaksets $DATA_DIR/clusters --color seagreen"
#
#  mk_pegs_intervals
run_test "mk_pegs_intervals" \
    --expected "refGene_mm10_intervals.bed" \
    --command "$MK_PEGS_INTERVALS $DATA_DIR/refGene_mm10.txt"
#
# Finished
report_tests
exit $?
##
#
