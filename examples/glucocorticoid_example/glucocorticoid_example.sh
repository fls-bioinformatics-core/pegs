#!/bin/bash

EXAMPLE_DIR=$(dirname $0)

echo $EXAMPLE_DIR

pegs mm10 \
  $EXAMPLE_DIR/data/peaks \
  $EXAMPLE_DIR/data/clusters \
  1000 5000 10000 50000 100000 200000 500000 1000000 5000000 \
  --tads $EXAMPLE_DIR/data/mESC-TADs_mm10.txt \
  --name glucocorticoid \
  -o $EXAMPLE_DIR/results
