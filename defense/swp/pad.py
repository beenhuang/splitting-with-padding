#!/usr/bin/env python3

"""
<file>    pad.py
<brief>   padding
"""

from math import ceil
import itertools
import random

from scipy.stats import geom, uniform, lognorm, weibull_min, genpareto, rayleigh

OUTGOING = 1
INCOMING = -1

# original trace: [[timestamp, direction], ...]
def padding(original_trace):
    inter_time_o2o = 0.0001

    client_consecutive_out = 0
    client_consecutive_in = 0

    c_br_loc, c_br_pack = client_break_params()
    r_br_loc, r_br_pack = relay_break_params()
    c_ex_pack = client_extend_param()
    r_ex_pack = relay_extend_param()

    #defended_trace = front_defend(original_trace)
    #defended_trace = first_fake_burst(original_trace)
    #defended_trace = sorted(defended_trace, key=lambda x:x[0]) 
    #return defended_trace

    delay = 0
    last_packet_time = 0.0
    last_packet_direction = OUTGOING
    rtt=0.12

    defended_trace = []
    for e in original_trace:
        defended_trace.append(e)

        packet_time = e[0]
        packet_direction = e[1]

        if last_packet_direction == OUTGOING and packet_direction == INCOMING: 
            rtt = float(packet_time - last_packet_time)

        # current packet is a outgoing packet
        if packet_direction == OUTGOING:
            client_consecutive_out += 1
            if client_consecutive_in != 0:
                client_consecutive_in = 0

            ## client extend burst
            if client_consecutive_out == 2 and uniform.rvs(size=1)[0] >= 0.7:  
            #if client_consecutive_out == 2: 
                time_c_ex = packet_time
                for _ in range(c_ex_pack): # client extend packets
                    time_c_ex += inter_time_o2o
                    defended_trace.append([time_c_ex, 222*OUTGOING])
                c_ex_pack = client_extend_param()                    

            # relay break burst
            if client_consecutive_out == r_br_loc: # r_br_loc
                time_r_br = packet_time + rtt/2
                for _ in range(r_br_pack): # r_br_pack
                    time_r_br += inter_time_o2o
                    defended_trace.append([time_r_br, 888*INCOMING])
                client_consecutive_out = 0       
                r_br_loc, r_br_pack = relay_break_params()  
                #print(f"r_pad_loc:{r_pad_loc}, r_pad_pack:{r_pad_pack}")

            last_packet_time = packet_time
            last_packet_direction = packet_direction

        elif e[1] == INCOMING:
            client_consecutive_in += 1
            if client_consecutive_out != 0:
                client_consecutive_out = 0 

            # relay extend burst
            if client_consecutive_in == 2 and uniform.rvs(size=1)[0] >= 0.9:
            #if client_consecutive_in == 2:  
                time_r_ex = packet_time
                for _ in range(r_ex_pack): # relay extend packets
                    time_r_ex += inter_time_o2o
                    defended_trace.append([time_r_ex, 444*INCOMING])
                r_ex_pack = relay_extend_param()

            ## client break burst
            if client_consecutive_in == c_br_loc: # c_pad_loc
                time_c_br = packet_time
                for _ in range(c_br_pack): # c_pad_pack
                    time_c_br += inter_time_o2o
                    defended_trace.append([time_c_br, 666*OUTGOING])
                client_consecutive_in = 0
                c_br_loc, c_br_pack = client_break_params()  
            #    print(f"c_pad_loc:{c_pad_loc}, c_pad_pack:{c_pad_pack}")

            last_packet_time = packet_time
            last_packet_direction = packet_direction
    #defended_trace = end_fake_burst(defended_trace)
    defended_trace = first_fake_burst(defended_trace)

    return regular_trace(defended_trace)

def regular_trace(trace):
    sorted_trace = sorted(trace, key=lambda x:x[0]) 

    ## Rescale since for a local adversary views the first packet starting at 0
    start_time = sorted_trace[0][0]
    for packet in sorted_trace:
        packet[0] = packet[0] - start_time 

    return sorted_trace    


def client_break_params():
    #c_br_loc = int(weibull_min.rvs(c=4.603295174042998, loc=0.9999999999999999, scale=4.603295174042998, size=1)[0])
    #c_br_pack = int(weibull_min.rvs(c=0.1090146228765905, loc=0.9999999999999999, scale=2.5784124861967372, size=1)[0])
    c_br_loc = int(rayleigh.rvs(loc=5.0100934937808645, scale=5.4042479185778625, size=1)[0])   
    c_br_pack = geom.rvs(p=0.6720704613633172, loc=0.0, size=1)[0]   
    
    # minimum
    c_br_loc = max(c_br_loc, 6)
    c_br_pack = max(c_br_pack, 1)

    # maximum
    c_br_loc = min(c_br_loc, 15)
    c_br_pack = min(c_br_pack, 4)

    return c_br_loc, c_br_pack

def relay_break_params():
    r_br_loc = int(rayleigh.rvs(loc=3.9520158881596017, scale=3.8923620672750783, size=1)[0])   
    r_br_pack = geom.rvs(p=0.45767131312950055, loc=0.0, size=1)[0]   

    # minimum
    r_br_loc = max(r_br_loc, 5)
    r_br_pack = max(r_br_pack, 1)

    # maximum
    r_br_loc = min(r_br_loc, 18)
    r_br_pack = min(r_br_pack, 6)

    return r_br_loc, r_br_pack

def client_extend_param():
    c_ex_pack = geom.rvs(p=0.6718020099927879, size=1)[0]

    # maximum
    c_ex_pack = min(c_ex_pack, 4)
    
    return c_ex_pack        

def relay_extend_param():
    r_ex_pack = geom.rvs(p=0.4571386203563751, size=1)[0]

    # maximum
    r_ex_pack = min(r_ex_pack, 5)

    return r_ex_pack 

def first_fake_burst(trace):
    curr_time = 1.00
    rtt = 0.0
    
    loop_num = random.randint(1, 20)
    #print(f"loop_num:{loop_num}")
    for _ in range(loop_num): # loop times
        # fake outgoing burst
        fake_client_outgoing = geom.rvs(p=0.7620060515717053, size=1)[0]
        fake_client_outgoing = min(fake_client_outgoing, 5)
        for _ in range(fake_client_outgoing): # fake outgoing packets
            curr_time += 0.0001*random.randint(1, 3)
            trace.append([curr_time, 555*OUTGOING])

        # fake incoming burst
        curr_time += random.uniform(0.100, 0.300)# o-i iat
        fake_client_incoming = int(rayleigh.rvs(loc=2.142881728007377, scale=2.998029777424256, size=1)[0]) # fake incoming packets
        fake_client_incoming = min(fake_client_incoming, 10)
        for _ in range(fake_client_incoming):
            curr_time = curr_time+0.0001*random.randint(1, 3)# i-i iat
            trace.append([curr_time, 777*INCOMING]) 

        curr_time += 0.5   

    return trace  


def end_fake_burst(defended_trace):
    last_time = defended_trace[-1][0]

    for i in range(random.randint(1, 5)): # loop times
        # fake outgoing burst
        if defended_trace[-1][1] == OUTGOING:
            last_time += 0.0001 # o-o iat
        else:
            last_time += 0.002 # i-o iat
        fake_client_outgoing = geom.rvs(p=0.7, size=1)[0]
        for _ in range(fake_client_outgoing): # fake outgoing packets
            last_time = last_time+0.0001 # o-o iat
            defended_trace.append([last_time, 555*OUTGOING])

        # fake incoming burst
        last_time += 0.0002 # o-i iat
        fake_client_incoming = geom.rvs(p=0.2, size=1)[0] # fake incoming packets
        for _ in range(fake_client_incoming):
            last_time = last_time+0.0001 # i-i iat
            defended_trace.append([last_time, 777*INCOMING]) 

    return defended_trace  



if __name__ == "__main__":
    def preprocess(trace, packet_size=514):
        start_time = float(trace[0].split("\t")[0])
  
        good_trace = []
        for e in trace:
            e = e.split("\t")
            time = float(e[0]) - start_time
            direction = int(e[1].strip("\n"))
            good_trace.append([time, direction])

        return good_trace

    with open("/Users/huangbin/desktop/paper3/data/Wang-20000/0-0.cell", "r") as f:
        trace = f.readlines() 

    good_trace = preprocess(trace)
    defended_trace = padding(good_trace)

    with open("/Users/huangbin/desktop/paper3/defense/huang/0-0.cell", "w") as f:
        for e in defended_trace:
            f.write(str(e[0])+"\t"+str(e[1])+"\n")   

    print(f"all done") 


    def burst_trace(original_trace):
        directions = [e[1] for e in original_trace]
        burst = [k*len(list(v)) for k,v in itertools.groupby(directions)]

        return burst

