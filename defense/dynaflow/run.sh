#!/bin/bash

# defense directory
dir=/home/shadow/paper3/defense
# data directory
data=Wang-20000
# defense algorithm
defense=dynaflow


echo "--------  run $defense --------"
  
  $dir/$defense/main.py --in $data --defense $defense

echo "----------  all done   ----------"