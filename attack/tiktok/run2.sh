#!/bin/bash

run=/home/shadow/paper3/attack/tiktok/run2.sh
# attack directory
dir=/home/shadow/paper3/attack
# WF attack
attack=tiktok
# data directory
data=bigenough/standard
# feature pickle file
feature=feature.pkl
# result file
result=bigenough-standard

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  $dir/$attack/extract.py --in $data --attack $attack
  $dir/$attack/classify_torch.py --in $data/$feature --out $result
  
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  $directory/classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

