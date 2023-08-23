#!/bin/bash

run=/home/shadow/paper3/attack/cumul/run.sh
# current directory
directory=/home/shadow/paper3/attack/cumul
# WF attack
attack=cumul
# WF defense
defense=bigenough
# trace directory
data=standard
# feature pickle file
feature=feature.pkl
result=aa

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  #$directory/extract.py --in $defense/$data --attack $attack
  $directory/classify.py --in $defense/$data/$feature --out ${defense}-$data
   
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  ./classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

