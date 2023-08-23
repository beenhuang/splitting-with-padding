#!/bin/bash

run=/home/shadow/paper3/evaluation/one-page/kfp/run.sh
# directory
dir=/home/shadow/paper3/evaluation/one-page/kfp
# WF attack
attack=kfp
# WF defense
defense=trafficsilver
# data directory
data=bigenough/safest-4
# feature pickle file
feature=feature.pkl
# result file
result=bigenough-safest-4

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  $dir/extract.py --in $defense/$data --attack $attack
  $dir/classify.py --in $defense/$data/$feature --out ${defense}-$result
   
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  ./classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

