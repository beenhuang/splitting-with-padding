#!/usr/bin/env python3

"""
<file>    huang.py
<brief>   huang defense
"""

import os
from os.path import exists, join

from split import splitting
from pad import padding

OUTGOING = 1
INCOMING = -1

def defend(trace, defended_dir, file):
    split_trace_0, split_trace_1 = splitting(trace)

    if split_trace_0 != -1:
        pad_trace_0 = padding(split_trace_0)
        save_in_file(pad_trace_0, defended_dir+"-0", file)
    if split_trace_1 != -1:
        pad_trace_1 = padding(split_trace_1)
        save_in_file(pad_trace_1, defended_dir+"-1", file)

def save_in_file(defended_trace, defended_dir, file):
    if not exists(defended_dir):
        os.makedirs(defended_dir)    

    # save the defended trace
    with open(join(defended_dir, file), "w") as f:
        for e in defended_trace:
            # timestamp, direction, num_path
            #f.write(str(e[0])+"\t"+str(e[1])+"\t"+str(e[2])+"\n")
            f.write(str(e[0])+"\t"+str(e[1])+"\n")

if __name__ == "__main__":
    def preprocess(trace, packet_size=514):
        start_time = float(trace[0].split("\t")[0])
        #logger.debug(f"start_time: {start_time}")
        
        good_trace = []
        for e in trace:
            e = e.split("\t")
            time = float(e[0]) - start_time
            direction = int(e[1].strip("\n"))
            good_trace.append([time, direction])

        #logger.debug(f"good_trace: {good_trace}")

        return good_trace

    file_path = "/Users/huangbin/desktop/WF-script/data/Wang-20000/0-0.cell"
    with open(file_path, "r") as f:
        trace = f.readlines() 
    
    defend(preprocess(trace), "", "")





