#!/bin/bash

# trace directory
data=Wang-20000
defend=swp

# trace directory
data2=swp/Wang-20000
# classication results
result=version2


echo "--------  run program --------"
  
  #./defense/main.py --in $data
  #./overhead/bandwidth.py --in $data --def $defend  
  #./attack/df/extract.py --in $defend/$data
  ./attack/df/classify.py --in $defend/$data/feature.pkl --out $result  

echo "----------  all done   ----------"


