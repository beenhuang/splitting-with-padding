#!/bin/bash

# attack directory
dir=/home/shadow/paper3/attack
# WF attack
attack=df
# WF defense
defense=front
# data directory
data=Wang-20000
# feature pickle file
feature=feature.pkl

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  $dir/$attack/extract.py --in $defense/$data --attack $attack
  $dir/$attack/classify_torch.py --in $defense/$data/$feature --out ${defense}-$data
  
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  $directory/classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

