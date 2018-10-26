import sys
sys.path.append('../module')

import socket
from datetime import datetime as dt
import pickle as pkl
import Gilbert as gl
import pandas as pd
import numpy as np
import math
import time
from joblib import Parallel,delayed
#--initial definition--#
MAX_SIZE = 4096
DATA_PATH = '../datasets/'
DATA_NUM_LIST = [300,500,700,1000,3000,5000,7000,10000,30000]
DIM = 10
EXPERIMENT = 100
EPSILON = 0.01
CONDITION = 10


#--address&port--#
HOST = 'localhost'
NODES = 60
PORT_LIST = []
for PORT in range(18400,18400+NODES):
    PORT_LIST.append(PORT)

#--access to each server--#
address = []
client = []
for PORT in PORT_LIST:
    address.append((HOST,PORT))
    client.append(socket.socket(socket.AF_INET,socket.SOCK_STREAM))
for i in range(NODES):
    client[i].connect(address[i])
    client[i].sendall(b'hello')
    log = client[i].recv(MAX_SIZE)


#--run for several datasets--#
for DATA_NUM in DATA_NUM_LIST:

    #--load datasets--#
    title = DATA_PATH + 'dataset' + str(DATA_NUM) + '_dist5_' + str(DIM) + 'dim.csv'
    dataset = pd.read_csv(title)

    #--devide origin&data--#
    origin = dataset.loc[0,:]
    data = pd.DataFrame(dataset[1:])
    SET_NUM = len(data)
    data = data.reset_index(drop=True)

    #--get set P (separate for nodes)--#
    EACH_SET = math.floor(SET_NUM / NODES)
    AMARI = SET_NUM % NODES
    set_P = []
    counter = 0
    amari_counter = 0
    for i in range(NODES):
        if amari_counter < AMARI:
            node_data = pd.DataFrame(data[counter:counter+EACH_SET+1])
            amari_counter +=1
        else:
            node_data = pd.DataFrame(data[counter:counter+EACH_SET])
        node_data = node_data.reset_index(drop=True)
        set_P.append(node_data)
        counter += EACH_SET
    #--send dataset--#
    b_data = []
    for i in range(NODES):
        b_data.append(pkl.dumps(set_P[i])) # to binary data
        client[i].sendall(b'dataset') #protocol
    for i in range(NODES):
        sign = gl.recvall(client[i])
        client[i].sendall(b_data[i]) #send data

    #--receive reply--#
    for i in range(NODES):
        sign = gl.recvall(client[i])

    #--step 1--#
    x1_list = []
    x1_L2_list = []
    for i in range(NODES):
        client[i].sendall(b'step1')
        b_x1 = gl.recvall(client[i])
        node_x1 = pkl.loads(b_x1)
        L2 = np.linalg.norm(node_x1)
        x1_list.append(node_x1)
        x1_L2_list.append(L2)

    x1_L2_list = np.array(x1_L2_list) #choose minimum
    x1 = x1_list[x1_L2_list.argmin()]
    p1 = x1

    #--loop params--#
    epsilon = EPSILON
    cond = CONDITION
    time_outline = []
    for e_num in range(EXPERIMENT):

        itr = 0
        total_time = 0
        #--step i--#
        newX = x1
        newP = [p1,0]

        while True:
            #calc time
            start_time = dt.now().strftime('%s')

            #send x
            b_newX = pkl.dumps(newX)
            for i in range(NODES):
                client[i].sendall(b'stepi')
                sign = gl.recvall(client[i])
                client[i].sendall(b_newX)

            #get newP
            newP_list = []
            PbarX_list = []
            for i in range(NODES):
                b_newP = gl.recvall(client[i])
                node_P = pkl.loads(b_newP)
                newP_list.append(node_P)
                PbarX_list.append(node_P[1])
            PbarX_list = np.array(PbarX_list)
            newP = newP_list[PbarX_list.argmin()] #choose min PbarX
            
            #check condition
            dist_X = np.linalg.norm(newX)
            cond = 1.0 - (newP[1]/dist_X)

            #calculate newX
            newX = gl.nextX(newP[0],newX)
            dist_newX = np.linalg.norm(newX)

            # less than epsilon
            if cond <= epsilon:
                break
            
            itr += 1

            end_time = dt.now().strftime('%s')
            total_time += int(end_time) - int(start_time)

        #--calc time--#
        avg_time = total_time / (itr + 1)
        time_outline.append(avg_time)

    #--message--#
    print('Point Set[%d]: Done.' % DATA_NUM)

    #--output--#
    output_title = '../result/pickle/Distributed/result_Distributed_' + str(DATA_NUM) + 'P.pkl'
    with open(output_title,'wb') as f:
        pkl.dump(time_outline,f)

#--end session--#
#send session ending command
for i in range(NODES):
    client[i].sendall(b'end')

