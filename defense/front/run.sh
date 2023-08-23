#!/bin/bash

run=/home/shadow/paper3/defense/front/run.sh
# current directory
directory=/home/shadow/paper3/defense
# trace directory
data=Wang-20000
defense=front


echo "--------  run $defense --------"
  
  $directory/$defense/main.py --in $data --defense $defense

echo "----------  all done   ----------"


