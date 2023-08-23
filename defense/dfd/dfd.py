#!/usr/bin/env python3

"""
<file>    dfd.py
<brief>   DFD defense
"""

import random
import numpy as np

# pert: the perturbation rate to be applied
pert = 0.50
# variation_ratio: the variation parameter, affect the perturbation rate at the begining of each burst, this will only effect the white-box attack accuracy. (0 < variation_ratio < 1.0)
variation_ratio = 0.5
# ServerSide: If True, server-side injection will also be used (True/False)
ServerSide = True
# ClientSide: If True, client-side injection will also be used (True/False)
ClientSide = True


# wrapper for DFD written by Author
def defend(trace):
    #directions = [x[1] for x in trace]
    return dfd(trace)

def dfd(X_test):
    Cout = 0
    Cin = 0
    last = 0

    OUTGOING = 1
    INCOMING = -1
    PAD_OUTGOING = 888*OUTGOING
    PAD_INCOMING = 444*INCOMING

    INTERVAL_O2O = 0.0001
    INTERVAL_I2I = 0.0001

    X_testN = []
    for j, _ in enumerate(X_test):
        X_testN.append(X_test[j])
        if X_test[j][1] == 0:
            continue
        else:
            perturbationCurrent = random.uniform(pert*variation_ratio, pert*(1+variation_ratio))
            if X_test[j][1] == OUTGOING: # outgoing
                Cout += 1
                if last == INCOMING:
                    if ClientSide:
                        toAppend = int(1+perturbationCurrent*Cin)
                        time = X_test[j][0]
                        for k in range(toAppend):
                            time += INTERVAL_I2I
                            X_testN.append([time, PAD_INCOMING])
                    Cin = 0
            elif X_test[j][1] == INCOMING: # incoming
                Cin += 1
                if last == OUTGOING :
                    if ServerSide:
                        toAppend = int(1+perturbationCurrent*Cout)
                        time = X_test[j][0]
                        for k in range(toAppend):
                            time += INTERVAL_O2O
                            X_testN.append([time, PAD_OUTGOING])
                    Cout = 0
        last = X_test[j][1] 

    return regular_trace(X_testN)       

def regular_trace(trace):
    sorted_trace = sorted(trace, key=lambda x:x[0]) 

    ## Rescale since for a local adversary views the first packet starting at 0
    start_time = sorted_trace[0][0]
    for packet in sorted_trace:
        packet[0] = packet[0] - start_time 

    return sorted_trace    

