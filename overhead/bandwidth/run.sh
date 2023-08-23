#!/bin/bash

run=/home/shadow/paper3/overhead/bandwidth/run.sh
# current directory
directory=/home/shadow/paper3/overhead/bandwidth
# defense
defense=huang
# trace directory
data=bigenough/safest-1
result=bigenough-safest-1

echo "-------- bandwidth overhead of $defense --------"

  $directory/main.py --in $defense/$data --out band-$defense-$result

echo "----------  all done   ----------"

