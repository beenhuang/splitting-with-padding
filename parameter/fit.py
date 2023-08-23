#!/usr/bin/env python3

"""
<file>    fit.py
<brief>   distribution fit to data
"""

import argparse
import os
import sys   
import time
import pickle
import itertools
import logging
import numpy as np
import multiprocessing as mp
from os.path import join, basename, abspath, dirname, pardir, isdir, splitext, exists 

from distribution import optimal_distribution
from plot import save_bar_plot, show_bar_plot2

def logger_and_arguments():
    # get logger
    logging.basicConfig(format="[%(asctime)s]>>> %(message)s", level=logging.INFO, datefmt = "%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger(splitext(basename(__file__))[0])
    
    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--in", required=True, help="load burst pickle.")
    parser.add_argument("-o", "--out", required=True, help="save results.")
    args = vars(parser.parse_args())

    return logger, args

def mon_unmon_split(bursts, labels):
    # sort
    unmon_index = labels.index(max(labels))

    mon_bursts = bursts[:unmon_index]
    unmon_bursts = bursts[unmon_index:]

    return mon_bursts, unmon_bursts                 

def make_burst_plot(bursts, file):
    all_bursts = np.concatenate(bursts).astype(int)
    send_burst = all_bursts[all_bursts > 0]
    recv_burst = -all_bursts[all_bursts < 0] 

    unique_total, count_total = np.unique(all_bursts, return_counts=True)
    unique_send, count_send = np.unique(send_burst, return_counts=True)
    unique_recv, count_recv = np.unique(recv_burst, return_counts=True)

    with open(file, "w") as f:
        for line in list(zip(unique_total, count_total)):
            f.write(str(line)+"\n") 

    #show_bar_plot2(unique_send[:15], count_send[:15], "SEND BURST", "burst size", "count")
    #show_bar_plot2(unique_recv[:15], count_recv[:15], "RECV BURST", "burst size", "count")     

    # save
    for max_index in range(10, 210, 10):
        save_bar_plot(unique_send[:max_index], count_send[:max_index], join(OUTPUT_DIR, f"{CURRENT_TIME}_send-{max_index}-{file}.png"), "SEND BURST", "send burst", "count")
        save_bar_plot(unique_recv[:max_index], count_recv[:max_index], join(OUTPUT_DIR, f"{CURRENT_TIME}_recv-{max_index}-{file}.png"), "RECV BURST", "recv burst", "count")     

def burst_distfit(bursts, file, max_index):
    all_bursts = np.concatenate(bursts).astype(int)
    send_burst = all_bursts[all_bursts > 0]
    recv_burst = -all_bursts[all_bursts < 0] 

    logger.info(f"max index: {max_index}")
    part_send_burst = send_burst[send_burst < max_index]
    part_recv_burst = recv_burst[recv_burst < max_index]

    optimal_distribution(part_send_burst, file+"-send.csv")
    optimal_distribution(part_recv_burst, file+"-recv.csv")
    
def main(X, y, result_file, max_index, PLOT=False):
    # make burst plot
    if PLOT:
        logger.info(f"MAKING burst plots ...")
        make_burst_plot(X, result_file)
        #make_burst_plot(mon_bursts, f"mon-{args['out']}")
        #make_burst_plot(unmon_bursts, f"unmon-{args['out']}")    
        sys.exit(0)

    # fit burst to distribution
    #logger.info(f"FITTING burst to the distribution ...")
    burst_distfit(X, result_file, max_index)

    #mon_bursts, unmon_bursts = mon_unmon_split(X, y)
    #logger.info(f"burst_trace -> total_length:{len(X)}, mon_length:{len(mon_bursts)}, unmon_length:{len(unmon_bursts)}")
    #burst_distfit(mon_bursts, result_file+"mon", max_index)
    #burst_distfit(unmon_bursts, result_file+"unmon", max_index)

if __name__ == "__main__":
    CURRENT_TIME = time.strftime("%Y.%m.%d-%H:%M:%S-", time.localtime())
    BASE_DIR = abspath(join(dirname(__file__), pardir))
    BURST_DIR = join(BASE_DIR, "parameter","burst-trace")
    OUTPUT_DIR = join(BASE_DIR, "parameter", "result")

    try:
        logger, args = logger_and_arguments()
        logger.info(f"{basename(__file__)} -> Arguments: {args}")

        burst_path = join(BURST_DIR, args["in"])
        with open(burst_path, "rb") as f:
            X, y = pickle.load(f)
            logger.info(f"[LOADED] dataset:{len(X)}, labels:{len(y)}")

        if not exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        result_file = join(OUTPUT_DIR, CURRENT_TIME+args["out"])

        main(X, y, result_file, int(args["out"]))

    except KeyboardInterrupt:
        sys.exit(-1)     

