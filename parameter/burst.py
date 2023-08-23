#!/usr/bin/env python3

"""
<file>    burst.py
<brief>   get brust trace
"""

import os
import sys
import pickle
import argparse
import logging
import numpy as np
import multiprocessing as mp
from os.path import abspath, dirname, join, pardir, splitext, basename, exists
import itertools

def logger_and_arguments():
    # get logger
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    # argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in", required=True, help="load data")
    args = vars(parser.parse_args())

    return logger, args

def preprocess(trace):
    good_trace = []

    for e in trace:
        e = e.split("\t")
        direction = int(e[1].strip("\n"))
        good_trace.append(direction)

    return good_trace

def burst(original_trace):
    burst = [k*len(list(v)) for k,v in itertools.groupby(original_trace)]

    return burst

def extract(data_dir, feature_dir, file, umon_label=100):
    # get file_name
    feature_fname = file.split(".")[0]
    print(f"feature_fname: {feature_fname}")

    # read a trace file.
    file_path = join(data_dir, file)
    with open(file_path, "r") as f:
        trace = f.readlines() 

    # X: trace    
    good_trace = preprocess(trace)  
    feature = burst(good_trace)
    # y: label
    label = int(umon_label) if "-" not in feature_fname else int(feature_fname.split("-")[0])

    # save the feature from the trace
    feature_path = join(feature_dir, feature_fname)
    with open(feature_path, "w") as f:
        for element in feature:
            f.write(f"{element}\n")

    return (feature, label) 
    
def main(data_dir, feature_dir, feature_pickle="burst.pkl"):
    flist = os.listdir(data_dir)
    params = [[data_dir, feature_dir, f] for f in flist]

    with mp.Pool(mp.cpu_count()) as pool:
        result = pool.starmap(extract, params)

    X, y = zip(*result) 
    with open(join(feature_dir, feature_pickle), "wb") as f:
        pickle.dump((X, y), f)    
    
if __name__ == "__main__":
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    DATA_DIR = join(BASE_DIR, "data")
    MAIN_FEATURE_DIR = join(BASE_DIR, "parameter", "burst-trace")

    try:
        logger, args = logger_and_arguments()
        logger.info(f"{basename(__file__)} -> Arguments: {args}")

        # input & output
        data_dir = join(DATA_DIR, args["in"])
        feature_dir = join(MAIN_FEATURE_DIR, args["in"])
        if not exists(feature_dir):
            os.makedirs(feature_dir)

        main(data_dir, feature_dir)    

    except KeyboardInterrupt:
        sys.exit(-1) 
