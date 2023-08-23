#!/bin/bash

# trace directory
data=Wang-20000
# burst pickle file
burst=burst.pkl
# classication results
result=40

echo "-------- distribution fitting --------"

  #./burst.py --in $data
  ./fit.py --in $data/$burst --out $result

echo "----------  all done   ----------"


