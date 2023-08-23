#!/usr/bin/env python3

"""
<file>    main.py
<brief>   
"""

import os
import sys
import time
import pickle
import logging
import argparse
import multiprocessing as mp
from os.path import abspath, dirname, join, pardir, splitext, basename, exists

from bandwidth import bandwidth_overhead

# logger and arguments
def logger_and_arguments():
    # get logger
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    # parse arguments
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-i", "--in", required=True, help="load trace data")
    parser.add_argument("-o", "--out", required=True, help="BO file name")
    args = vars(parser.parse_args())

    return logger, args

def preprocess(trace): 
    OUTGOING = 1
    INCOMING = -1

    real_sent, pad_sent, real_recv, pad_recv = 0, 0, 0, 0
    for e in trace:
        e = e.split("\t")
        direction = int(e[1].strip("\n"))

        if direction == OUTGOING:
            real_sent += 1
        elif direction == INCOMING:
            real_recv += 1
        elif direction > OUTGOING:
            pad_sent += 1
        elif direction < INCOMING:
            pad_recv += 1
        else:
            print(f"ERROR: unrecognized direction:{direction}") 

    return (real_sent, pad_sent, real_recv, pad_recv)

def extract(data_dir, bandwith_dir, file):
    print(f"extracting: {file}")
    # read a trace file.
    with open(join(data_dir, file), "r") as f:
        trace = f.readlines() 

    # get bandwidth
    element4 = preprocess(trace)  

    # save the bandwidth from the trace
    key = ["real_sent", "pad_sent", "real_recv", "pad_recv"]
    #with open(join(bandwidth_dir, file), "w") as f:
    #    for i, e in enumerate(element4):
    #        f.write(f"{key[i]}:{e}\n")

    return element4   

def bandwidth_total(bandwidth, bo_file_path):
    real_sent = sum([x[0] for x in bandwidth])
    pad_sent = sum([x[1] for x in bandwidth])
    real_recv = sum([x[2] for x in bandwidth])
    pad_recv = sum([x[3] for x in bandwidth])

    lines = bandwidth_overhead(real_sent, pad_sent, real_recv, pad_recv)

    with open(bo_file_path, "w") as f:
        f.writelines(lines)

# extract features one by one.
def main2(data_dir, bandwidth_dir, bo_file_path):
    flist = os.listdir(data_dir)

    bandwidth = []
    #for file in tqdm(flist, total=len(flist)):
    for file in flist:
        b = extract(data_dir, bandwidth_dir, file)
        bandwidth.append(b)
    
    bandwidth_total(bandwidth, bo_file_path)

    logger.info(f"Complete")  

# use multiprocessing
def main(data_dir, feature_dir, bo_file_path):
    flist = os.listdir(data_dir)
    params = [[data_dir, feature_dir, file] for file in flist]

    with mp.Pool(mp.cpu_count()) as pool:
        bandwidth = pool.starmap(extract, params)
  
    bandwidth_total(bandwidth, bo_file_path)

    logger.info(f"Complete")     

if __name__ == "__main__":
    CURRENT_TIME = time.strftime("%Y.%m.%d-%H:%M:%S", time.localtime())
    BASE_DIR = abspath(join(dirname(__file__), pardir, pardir))
    MAIN_DATA_DIR = join(BASE_DIR, "data")
    MAIN_RESULT_DIR = join(BASE_DIR, "overhead", "bandwidth", "result")

    try:
        logger, args = logger_and_arguments()
        logger.info(f"Arguments: {args}")

        data_dir = join(MAIN_DATA_DIR, args["in"])   

        bandwidth_dir = join(MAIN_RESULT_DIR, args["in"])
        if not exists(bandwidth_dir):
            os.makedirs(bandwidth_dir)
        
        bo_file_path = join(join(MAIN_RESULT_DIR, args["out"]+".txt"))
        
        main(data_dir, bandwidth_dir, bo_file_path)    

    except KeyboardInterrupt:
        sys.exit(-1) 
