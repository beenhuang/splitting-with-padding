#!/bin/bash

run=/home/shadow/paper3/attack/tiktok/run.sh
# attack directory
dir=/home/shadow/paper3/attack
# WF attack
attack=tiktok
# WF defense
defense=huang
# data directory
data=bigenough/safest-0
# feature pickle file
feature=feature.pkl
# result file
result=bigenough-safest-0

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  $dir/$attack/extract.py --in $defense/$data --attack $attack
  $dir/$attack/classify_torch.py --in $defense/$data/$feature --out ${defense}-$result
  
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  $directory/classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

