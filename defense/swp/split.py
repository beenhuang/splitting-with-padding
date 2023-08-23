#!/usr/bin/env python3

"""
<file>    huang.py
<brief>   huang defense
"""

import os
import sys
import random
import numpy as np
from os.path import exists, join, basename

OUTGOING = 1
INCOMING = -1

# 
def splitting(trace):
    #print(f"processing: {basename(file_path)}")
    
    paths = 2
    #batch_size_range = [50, 70]
    batch_size_range = [40, 60]
    alpha = [1, 1]
    # splitting strategy
    routes=batched_weighted_random(trace, paths, batch_size_range, alpha)
    
    # multi-path latency
    latency_file = "/home/shadow/paper3/defense/huang/circuits_latencies.txt"
    multi_path_latencies = get_circuit_latencies(paths, latency_file)
    
    # Simulate the multipath effect for the given latencies and routes
    defened_trace = simulate(trace, multi_path_latencies, routes) 
    trace_0, trace_1 = split_trace(defened_trace)
    

    return (regular_trace(trace_0), regular_trace(trace_1))

def simulate(trace, mplatencies, routes):   
    # Delta time to introduce as the time between two cells are sent from the end side
    inter_time_o2o = 0.0001 # interval_time_o2o
    delay = 0
    last_time = 0 
    last_time_incoming = 0
    last_packet_direction = OUTGOING 

    new_trace = []
    #Iterate over each packet
    for i, packet in enumerate(trace):
        packet_time = packet[0]
        packet_direction = packet[1]
        
        # Get the route according to the scheme
        route = routes[i]
        # Get the latency for this route
        chosen_latency = float(random.choice(mplatencies[(route%len(mplatencies))]))
        
        if (last_packet_direction != packet_direction): 
            #Calculate the RTT/2 (latency) request/response
            delay = float(packet_time - last_time) / 2 

        if (packet_direction == INCOMING):
            new_packet=[packet_time-delay+chosen_latency, packet_direction, route]
        # If is the first out in the burst, it referes to the last icomming time
        elif (last_packet_direction == INCOMING and packet_direction == OUTGOING): 
            new_packet=[last_time_incoming+inter_time_o2o, packet_direction, route]
        # If we are in an out burst, refers to the last out
        elif (last_packet_direction == OUTGOING and packet_direction == OUTGOING): 
            new_packet=[last_time+inter_time_o2o, packet_direction, route]
        new_trace.append(new_packet)

        last_time_incoming = packet_time-delay+chosen_latency
        last_time = packet_time
        last_packet_direction = packet_direction    

    return new_trace

def regular_trace(trace):
    if len(trace) == 0:
        return -1

    sorted_trace = sorted(trace, key=lambda x:x[0]) 

    ## Rescale since for a local adversary views the first packet starting at 0
    start_time = sorted_trace[0][0]
    for packet in sorted_trace:
        packet[0] = packet[0] - start_time 

    return sorted_trace    


def batched_weighted_random(trace, n, batch_size_range, alpha):
    #print("Simulating BWR multi-path scheme...")
    batch_low = batch_size_range[0]
    batch_high = batch_size_range[1]

    w_out = weights_of_paths(n, alpha)
    w_in = weights_of_paths(n, alpha)

    routes_client = []
    routes_server = []
    sent_incoming = 0
    sent_outgoing = 0
    last_client_route =  np.random.choice(np.arange(0,n), p=w_out)
    last_server_route = np.random.choice(np.arange(0,n), p=w_in)
    
    for packet in trace:
        direction = packet[1]

        if (direction == OUTGOING):
            routes_server.append(INCOMING) # Just to know that for this packet the exit does not decide the route
            sent_outgoing += 1
            C = random.randint(batch_low, batch_high) #After how many cells the scheduler sets new weights
            routes_client.append(last_client_route) 
            if (sent_outgoing % C == 0): #After C cells are sent, change the circuits
                        last_client_route = np.random.choice(np.arange(0,n), p=w_out)

        elif (direction == INCOMING): 
            routes_client.append(INCOMING) # Just to know that for this packet the client does not decide the route
            routes_server.append(last_server_route)
            sent_incoming += 1
            C = random.randint(batch_low, batch_high) #After how many cells the scheduler sets new weights
            if (sent_incoming % C == 0): #After C cells are sent, change the circuits
                 last_server_route = np.random.choice(np.arange(0,n), p=w_in)

    routes = joingClientServerRoutes(routes_client,routes_server)
    
    return routes

def weights_of_paths(paths, alpha):
    if (paths != len(alpha)):
        sys.exit(f"ERROR: paths:{paths} != alpha:{len(alpha)}")
        return -1

    return np.random.dirichlet(alpha,size=1)[0]

#joing the routes choosed by client and server into one route to be used by the simulate funtions
def joingClientServerRoutes(c,s): 
    if len(c)!= len(s):
        sys.exit("ERROR: Client and Server routes must have the same length")
    
    out = []
    for i in range(len(c)):
        if (c[i]==-1):
            out.append(s[i])
        elif (s[i]==-1):
            out.append(c[i])
    
    return out
    

def get_circuit_latencies(paths, latency_file):
    with open(latency_file, "r") as f:
        row_latencies = f.readlines()
    row_latencies = [e.strip("\n").split(" ") for e in row_latencies]

    num_of_clients = int(row_latencies[-1][0]) # 681
    random_client = random.randint(1, num_of_clients)
    
    multipath_latencies = []
    for latency in row_latencies:
        client_id = int(latency[0])
        if (client_id == random_client):
            multipath_latencies.append(latency[2].split(","))  
    # shuffle the elements of list, max of paths = 6
    random.shuffle(multipath_latencies)
    
    return multipath_latencies[0:paths]

def split_trace(trace):
    trace_1, trace_2 = [], []

    for packet in trace:
        if packet[2] == 0:
            trace_1.append(packet)
        elif packet[2] == 1:
            trace_2.append(packet)

    return (trace_1, trace_2)        
   
if __name__ == '__main__':
    paths = 5
    latencies = "/Users/huangbin/desktop/WF-script/defense/trafficsilver/circuits_latencies_new.txt"
    traces = "/Users/huangbin/desktop/WF-script/data/Wang-20000"
    outfolder = "/Users/huangbin/desktop/WF-script/defense/trafficsilver/out"
    range_ = "50, 70"
    alpha = "1,1,1,1,1"
