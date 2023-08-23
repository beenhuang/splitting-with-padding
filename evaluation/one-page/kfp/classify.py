#!/usr/bin/env python3

"""
<file>    classify.py
<brief>   classify website fingerprints.
"""

import os
import sys
import time
import pickle
import logging
import argparse
from os.path import join, basename, abspath, splitext, dirname, pardir, isdir, exists
from sklearn.model_selection import train_test_split

from metrics import *

# logger and arguments
def logger_and_arguments():
    # get logger
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    # parse arugment
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--in", required=True, help="load the feature.pkl")
    parser.add_argument("-o", "--out", required=True, help="save the result")
    args = vars(parser.parse_args())

    return logger, args

####

import random
import numpy as np
from kfp_classifier import train_kfp, test_kfp

MAX_INST=200

def one_mon_one_unmon(X, y, mon_label, unmon_label, max_inst=MAX_INST):
    data = [[X[i], y[i]] for i in range(len(y))]
    n = 0

    X_op, y_op = [], []
    random.shuffle(data)
    #print(f"data:{data}")
    for idx, e in enumerate(data):
        if mon_label == e[1]:
            X_op.append(e[0])
            y_op.append(e[1])
        
        if unmon_label == e[1] and n < max_inst:
            n += 1
            X_op.append(e[0])
            y_op.append(e[1])

    return X_op, y_op  

def main(X, y, result_path):
    #print(f"y:{y}")
    labels = np.unique(y)
    #print(f"labels:{labels}")
    mon_labels = labels[:-1]
    unmon_label = labels[-1]
    logger.info(f"mon_label:{mon_labels}, unmon_label:{unmon_label}")

    n = 0 
    acc, pre, tpr, fpr = 0.0, 0.0, 0.0, 0.0
    for mon_label in mon_labels:
        print(f"processing mon_label:{mon_label}")
        X_op, y_op = one_mon_one_unmon(X, y, mon_label, unmon_label)
        logger.info(f"X_op:{len(X_op)}, y_op:{len(y_op)}, labels:{list(set(y_op))}")

        # split dataset
        X_train, X_test, y_train, y_test = train_test_split(X_op, y_op, test_size=0.2, random_state=247, stratify=y_op)

        # training
        model, labeled_fps = train_kfp(X_train, y_train)
        # test
        y_pred = test_kfp(model, labeled_fps, X_test)
    
        # get metrics value
        lines, tmp_acc, tmp_pre, tmp_tpr, tmp_fpr = binary_score(y_test, y_pred, unmon_label)
        if tmp_acc != -1 and tmp_pre != -1 and tmp_tpr != -1 and tmp_fpr != -1 and tmp_acc != 0.0 and tmp_pre != 0.0 and tmp_tpr != 0.0 and tmp_fpr != 0.0:
            n += 1
            acc += tmp_acc 
            pre += tmp_pre 
            tpr += tmp_tpr 
            fpr += tmp_fpr 

        with open(result_path, "a") as f:
            f.write(f"mon_label:{mon_label}\n")
            f.writelines(lines)

    # average tpr/fpr
    num_mon = len(mon_labels)
    avg_value = f"avg_Acc:{acc/n}, avg_Pre:{pre/n}, avg_TPR:{tpr/n}, avg_FPR:{fpr/n}, num_loop:{n}\n"
    with open(result_path, "a") as f:
            f.write(avg_value)   

if __name__ == "__main__":
    CURRENT_TIME = time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())
    BASE_DIR = abspath(join(dirname(__file__)))
    FEATURE_DIR = join(BASE_DIR, "feature")
    RESULT_DIR = join(BASE_DIR, "result")

    logger, args = logger_and_arguments()
    logger.info(f"Arguments: {args}")

    feature_path = join(FEATURE_DIR, args["in"])
    with open(feature_path, "rb") as f:
        X, y = pickle.load(f)
        logger.info(f"X:{len(X)}, y:{len(y)}")

    if not exists(RESULT_DIR):
        os.makedirs(RESULT_DIR)
    result_path = join(RESULT_DIR, args["out"]+".txt")

    main(X, y, result_path)

    logger.info(f"Complete!")




