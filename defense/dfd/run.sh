#!/bin/bash

run=/home/shadow/paper3/defense/dfd/run.sh
# current directory
directory=/home/shadow/paper3/defense
# trace directory
data=bigenough/safest
defense=dfd


echo "--------  run $defense --------"
  
  $directory/$defense/main.py --in $data --defense $defense

echo "----------  all done   ----------"
