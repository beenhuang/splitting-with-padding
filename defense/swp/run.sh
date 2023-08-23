#!/bin/bash

run=/home/shadow/paper3/defense/swp/run.sh
# defense directory
dir=/home/shadow/paper3/defense
# data directory
data=bigenough/safest
# defense algorithm
defense=swp


echo "--------  run $defense --------"
  
  $dir/$defense/main.py --in $data --defense $defense

echo "----------  all done   ----------"