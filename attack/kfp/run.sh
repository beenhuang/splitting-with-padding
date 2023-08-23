#!/bin/bash

run=/home/shadow/paper3/attack/kfp/run.sh
# directory
directory=/home/shadow/paper3/attack/kfp
# WF attack
attack=kfp
# WF defense
defense=
# data directory
data=bigenough/standard
# feature pickle file
feature=feature.pkl
result=bigenough-standard

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  #$directory/extract.py --in $data --attack $attack
  $directory/classify.py --in $data/$feature --out $result
   
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  ./classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

