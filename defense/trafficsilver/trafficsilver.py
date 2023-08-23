# Code for simulating traffic-splitting strategies
# Used in: https://dl.acm.org/doi/10.1145/3372297.3423351
# Wladimr De la Cadena

#wdlc: Simulator of multipath effect over wang-style instances, IMPORTANT!!! use files in WANG Format with .cell extension. Three colums can be considered for each packet in the .cell file timestamp|direction|size
#Working methods Random, RoundRobin, Weighted Random and Batched Weighted Random and their variation to variable number of paths during the same page load. 

import numpy as np
import random
import multipath
import os
from os.path import exists, join, basename

# wrapper for sim_bwr()
def defend(file_path, defended_dir):
        paths = 5
        latencies = "/home/shadow/paper3/defense/trafficsilver/circuits_latencies_new.txt"
        range_ = "50, 70"
        alpha = "1,1,1,1,1"

        sim_bwr(paths, latencies, file_path, defended_dir, range_, alpha)
        #sim_br(paths, latencies, file_path, defended_dir, range_)
        #sim_bwr_blocked(paths, latencies, file_path, defended_dir, range_, alpha)
def sim_bwr(n, latencies, instance_file, outfiles, range_, alphas):
    #print("Simulating BWR multi-path scheme...")
    #traces_file = natsorted(glob.glob(traces[0]+'/*.cell'))
    ranlow = int(range_.split(',')[0])
    ranhigh = int(range_.split(',')[1])

    w_out = multipath.getWeights(n, alphas)
    w_in = multipath.getWeights(n, alphas)
    instance = open(instance_file,'r')
    instance = instance.read().split('\n')[:-1]
    mplatencies = getCircuitLatencies(latencies, n) # it is a list of list of latencies for each of m circuits. length = m
    routes_client = []
    routes_server = []
    sent_incomming = 0
    sent_outgoing = 0
    #print(f"n:{n}, w_out:{w_out}")
    last_client_route =  np.random.choice(np.arange(0,n),p = w_out)
    last_server_route = np.random.choice(np.arange(0,n),p = w_in)
    for i in range(0,len(instance)):
        packet = instance[i]
        packet = packet.replace(' ','\t') #For compatibility when data is space sperated not tab separated
        direction = multipath.getDirfromPacket(packet)

        if (direction == 1):
            routes_server.append(-1) # Just to know that for this packet the exit does not decide the route
            sent_outgoing += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            routes_client.append(last_client_route) 
            if (sent_outgoing % C == 0): #After C cells are sent, change the circuits
                        last_client_route =  np.random.choice(np.arange(0,n),p = w_out)

        if (direction == -1): 
            routes_client.append(-1) # Just to know that for this packet the client does not decide the route
            routes_server.append(last_server_route)
            sent_incomming += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            if (sent_incomming % C == 0): #After C cells are sent, change the circuits
                 last_server_route = np.random.choice(np.arange(0,n),p = w_in)


    routes = multipath.joingClientServerRoutes(routes_client,routes_server)
    ##### Routes Created, next to the multipath simulation
    new_instance = multipath.simulate(instance,mplatencies,routes) # Simulate the multipath effect for the given latencies and routes
    saveInFile(instance_file,new_instance,routes,outfiles)

def sim_bwr_blocked(n, latencies, instance_file, outfiles, range_, alphas):
    #print("Simulating BWR multi-path scheme...")
    #traces_file = natsorted(glob.glob(traces[0]+'/*.cell'))
    ranlow = int(range_.split(',')[0])
    ranhigh = int(range_.split(',')[1])

    w_out = multipath.getWeights(n, alphas)
    w_in = multipath.getWeights(n, alphas)
    instance = open(instance_file,'r')
    instance = instance.read().split('\n')[:-1]
    mplatencies = getCircuitLatencies(latencies, n) # it is a list of list of latencies for each of m circuits. length = m
    routes_client = []
    routes_server = []
    sent_incomming = 0
    sent_outgoing = 0
    #print(f"n:{n}, w_out:{w_out}")
    last_client_route =  np.random.choice(np.arange(0,n),p = w_out)
    last_server_route = np.random.choice(np.arange(0,n),p = w_in)
    for i in range(0,len(instance)):
        packet = instance[i]
        packet = packet.replace(' ','\t') #For compatibility when data is space sperated not tab separated
        direction = multipath.getDirfromPacket(packet)

        if (direction == 1):
            routes_server.append(-1) # Just to know that for this packet the exit does not decide the route
            sent_outgoing += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            routes_client.append(last_client_route) 
            if (sent_outgoing % C == 0): #After C cells are sent, change the circuits
                while(1):
                    client_route =  np.random.choice(np.arange(0,n),p = w_out)
                    if (client_route != last_client_route):
                        last_client_route = client_route
                        break # In this way, we block the possibility of choosing the same circuit previously chosen

        if (direction == -1): 
            routes_client.append(-1) # Just to know that for this packet the client does not decide the route
            routes_server.append(last_server_route)
            sent_incomming += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            if (sent_incomming % C == 0): #After C cells are sent, change the circuits
                while(1):
                    server_route =  np.random.choice(np.arange(0,n),p = w_in)
                    if (server_route != last_server_route):
                        last_server_route = server_route
                        break # In this way, we block the possibility of choosing the same circuit previously chosen

    routes = multipath.joingClientServerRoutes(routes_client,routes_server)
    ##### Routes Created, next to the multipath simulation
    new_instance = multipath.simulate(instance,mplatencies,routes) # Simulate the multipath effect for the given latencies and routes
    saveInFile(instance_file,new_instance,routes,outfiles)

def sim_br(n, latencies, instance_file, outfiles, range_):
    #print("Simulating BWR multi-path scheme...")
    #traces_file = natsorted(glob.glob(traces[0]+'/*.cell'))
    ranlow = int(range_.split(',')[0])
    ranhigh = int(range_.split(',')[1])

    instance = open(instance_file,'r')
    instance = instance.read().split('\n')[:-1]
    mplatencies = getCircuitLatencies(latencies, n) # it is a list of list of latencies for each of m circuits. length = m
    routes_client = []
    routes_server = []
    sent_incomming = 0
    sent_outgoing = 0
    #print(f"n:{n}, w_out:{w_out}")
    last_client_route =  np.random.choice(np.arange(0,n))
    last_server_route = np.random.choice(np.arange(0,n))
    for i in range(0,len(instance)):
        packet = instance[i]
        packet = packet.replace(' ','\t') #For compatibility when data is space sperated not tab separated
        direction = multipath.getDirfromPacket(packet)

        if (direction == 1):
            routes_server.append(-1) # Just to know that for this packet the exit does not decide the route
            sent_outgoing += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            routes_client.append(last_client_route) 
            if (sent_outgoing % C == 0): #After C cells are sent, change the circuits
                        last_client_route =  np.random.choice(np.arange(0,n))

        if (direction == -1): 
            routes_client.append(-1) # Just to know that for this packet the client does not decide the route
            routes_server.append(last_server_route)
            sent_incomming += 1
            C = random.randint(ranlow,ranhigh) #After how many cells the scheduler sets new weights
            if (sent_incomming % C == 0): #After C cells are sent, change the circuits
                 last_server_route = np.random.choice(np.arange(0,n))


    routes = multipath.joingClientServerRoutes(routes_client,routes_server)
    ##### Routes Created, next to the multipath simulation
    new_instance = multipath.simulate(instance,mplatencies,routes) # Simulate the multipath effect for the given latencies and routes
    saveInFile(instance_file,new_instance,routes,outfiles)

def getCircuitLatencies(l,n):
    file_latencies = open(l,'r')
    row_latencies = file_latencies.read().split('\n')[:-1]
    numberOfClients = int(row_latencies[-1].split(' ')[0])
    randomclient = random.randint(1,numberOfClients)
    ## Get the multiple circuits of the selected client:
    multipath_latencies = []
    for laten in row_latencies:
        clientid = int(laten.split(' ')[0])
        if (clientid == randomclient):
            multipath_latencies.append(laten.split(' ')[2].split(','))	
    ## I only need n circuits, it works when n <  number of circuits in latency file (I had max 6)
    multipath_latencies = multipath_latencies[0:n]
    return multipath_latencies

def saveInFile2(input_name,split_inst,r,outfolder):
    numberOfFiles = max(r)+1 # How many files, one per route
    outfiles = []
    for k in range(0,numberOfFiles):
        input_name2 = input_name.split('.cell')[0].split('/')[-1]
        out_file_name = outfolder + "/" + input_name2 + "_split_" + str(k) + '.cell'
        outfiles.append(open(out_file_name,'w'))

    jointfilename = outfolder + "/" + input_name.split('.cell')[0].split('/')[-1] + "_join"+ '.cell'
    jointfile = open (jointfilename,'w')
    for i in range(0,len(split_inst)):
        x_arrstr = np.char.mod('%.15f', split_inst[i][:-1])
        x_arrstr[1] = int(float(x_arrstr[1]))
        jointfile.write('\t'.join(x_arrstr) + '\n')

    fs = [0] * numberOfFiles
    ts_o = [0] * numberOfFiles
    for i in range(0,len(split_inst)):
        rout = int(split_inst[i][3])
        if (fs[rout] == 0):
            ts_o[rout] = float(split_inst[i][0])
        fs[rout] = 1
        x_arrstr = np.char.mod('%.15f', split_inst[i])
        x_arrstr[1] = int(float(x_arrstr[1]))
        x_arrstr = x_arrstr.astype(float)
        strwrt =  str(x_arrstr[0] - ts_o[rout]) + '\t' + str(int(x_arrstr[1])) + '\t' + str(x_arrstr[2])
        outfiles[rout].write(strwrt+ '\n')      

def saveInFile(input_name, split_inst, r, outfolder):
    numberOfFiles = max(r)+1 # How many files, one per route
    outfiles = []
    for k in range(numberOfFiles):
        input_name2 = input_name.split('.cell')[0].split('/')[-1]
        out_fil_dir = outfolder + "-" + str(k)
        if not exists(out_fil_dir):
            os.makedirs(out_fil_dir)
        
        out_file_name = out_fil_dir + "/" + input_name2 + '.cell'
        #print(f"out_file_name: {out_file_name}")
        outfiles.append(open(out_file_name,'w'))

    jointfile_dir = outfolder + "-join"
    if not exists(jointfile_dir):
        os.makedirs(jointfile_dir)
    jointfilename = jointfile_dir + "/" + input_name.split('.cell')[0].split('/')[-1] + '.cell'
    jointfile = open (jointfilename,'w')
    for i in range(0,len(split_inst)):
        x_arrstr = np.char.mod('%.15f', split_inst[i][:-1])
        x_arrstr[1] = int(float(x_arrstr[1]))
        jointfile.write('\t'.join(x_arrstr) + '\n')

    fs = [0] * numberOfFiles
    ts_o = [0] * numberOfFiles
    for i in range(0,len(split_inst)):
        rout = int(split_inst[i][3])
        if (fs[rout] == 0):
            ts_o[rout] = float(split_inst[i][0])
        fs[rout] = 1
        x_arrstr = np.char.mod('%.15f', split_inst[i])
        x_arrstr[1] = int(float(x_arrstr[1]))
        x_arrstr = x_arrstr.astype(float)
        strwrt =  str(x_arrstr[0] - ts_o[rout]) + '\t' + str(int(x_arrstr[1])) + '\t' + str(x_arrstr[2])
        outfiles[rout].write(strwrt+ '\n')      

def saveInFile3(input_name,split_inst,r,outfolder):
    numberOfFiles = max(r)+1 # How many files, one per route
    outfiles = []
    for k in range(0,numberOfFiles):
        out_dir = outfolder + "-" + str(k)
        if not exists(out_dir):
            os.makedirs(out_dir)

        out_file_path = join(out_dir, basename(input_name))
        outfiles.append(open(out_file_path,'w'))
    
    print(f"{outfiles}")
    fs = [0] * numberOfFiles
    ts_o = [0] * numberOfFiles
    # traverse cells from trace
    for e in split_inst:
        #print(f"{split_inst}")
        rout = int(e[3]) # path_num
        print(f"rout:{rout}")
        if (fs[rout] == 0):
            ts_o[rout] = float(e[0]) # timestamp
            fs[rout] = 1

        timestamp = e[0] - ts_o[rout]
        direction = int(e[1])   
        path = int(e[2])
        strwrt =  str(timestamp) + '\t' + str(direction) + '\t' + str(path)+ '\n'
        outfiles[rout].write(strwrt)      
 
   
if __name__ == '__main__':
    paths = 5
    latencies = "/Users/huangbin/desktop/WF-script/defense/trafficsilver/circuits_latencies_new.txt"
    traces = "/Users/huangbin/desktop/WF-script/data/Wang-20000"
    outfolder = "/Users/huangbin/desktop/WF-script/defense/trafficsilver/out"
    range_ = "50, 70"
    alpha = "1,1,1,1,1"

    sim_bwr(paths, latencies, traces,outfolder,range_, alpha)
