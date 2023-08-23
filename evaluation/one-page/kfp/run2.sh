#!/bin/bash

run=/home/shadow/paper3/evaluation/one-page/kfp/run2.sh
# directory
dir=/home/shadow/paper3/evaluation/one-page/kfp
# WF attack
attack=kfp
# data directory
data=bigenough/standard
# feature pickle file
feature=feature.pkl
# result file
result=bigenough-standard

echo "-------- run $attack script --------"
  echo "-------- extract ${attack}'s features --------"
  $dir/extract.py --in $data --attack $attack
  $dir/classify.py --in $data/$feature --out $result
   
#for i in {1..10}
#do
#  echo "-------- ${i}th classification --------"
#  ./classify_torch.py --in $data/$feature --out $result
#done 

echo "----------  all done   ----------"

