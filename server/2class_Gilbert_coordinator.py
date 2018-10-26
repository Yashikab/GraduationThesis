import sys
sys.path.append('../module')

import socket
from datetime import datetime as dt
import pickle as pkl
import Gilbert as gl
import twoclassalg as alg
import pandas as pd
import numpy as np
import math
import time
#--read file--#
DATA_NUM = 5
DATA_PATH = '../datasets/pickle/2class_d/'
DIM = 10
NUM = 10000
MARGIN_LIST = [0.1,0.2,0.3]
DATASET_LIST = [[] for i in range(DATA_NUM)]
ANS_DBS_LIST = [[] for i in range(DATA_NUM)]
for i in range(DATA_NUM):
    for m in MARGIN_LIST:    
        title = DATA_PATH + '2class_dataset'+ str(NUM) +'P_'+ str(DIM) + 'dim_' + str(m) + 'M_' + str(i) + '.pkl'
        with open(title,'rb') as f:
            dataset, ans_DBS = pkl.load(f)
        DATASET_LIST[i].append(np.array(dataset))
        ANS_DBS_LIST[i].append(np.array(ans_DBS))

EPSILON = 0.01
CONDITION = 10


#--address&port--#
MAX_SIZE = 4096
HOST = 'localhost'
NODES = 4
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
    client[i].sendall(b'2class')
    log = client[i].recv(MAX_SIZE)


#--devide origin&data--#
data = np.array(DATASET_LIST[0][2])
SET_NUM = len(data)

#--get set P (separate for nodes)--#
set_P = [[] for i in range(NODES)]
for i in range(SET_NUM):
    set_P[i%NODES].append(data[i])


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
#initial point#
for d in data:
    if d[DIM] == 1:
        x11 = d[0:DIM]
        break
b_x11 = pkl.dumps(x11)
x21_list = []
x21_L2_list = []
for i in range(NODES):
    client[i].sendall(b'step1')
    sign = gl.recvall(client[i])
    client[i].sendall(b_x11)
    b_x21 = gl.recvall(client[i])
    node_x21 = pkl.loads(b_x21)
    L2 = np.linalg.norm(node_x21-x11)
    x21_list.append(node_x21)
    x21_L2_list.append(L2)

x21_L2_list = np.array(x21_L2_list) #choose minimum
x21 = x21_list[np.argmin(x21_L2_list)]

#--loop params--#
epsilon = EPSILON
counter = 0

#--step i--#
A_flag = True
B_flag = True
now_x1 = x11
now_x2 = x21

#start_time = dt.now().strftime('%s')
while (A_flag or B_flag):

    #-- update class A--#
    if A_flag:
        dist = np.linalg.norm(now_x1 - now_x2)
        b_newX = pkl.dumps((now_x1,now_x2,'A'))
        for i in range(NODES):
            client[i].sendall(b'stepi')
            sign = gl.recvall(client[i])
            client[i].sendall(b_newX)
        #get newP
        newP_list = []
        PbarX_list = []
        for i in range(NODES):
            b_newP = gl.recvall(client[i])
            node_P,node_PbarX = pkl.loads(b_newP)
            newP_list.append(node_P)
            PbarX_list.append(node_PbarX)
        PbarX_list = np.array(PbarX_list)
        newP = newP_list[np.argmin(PbarX_list)] #choose min PbarX
        newPbarX = np.min(PbarX_list)
                
        if 1 - newPbarX/dist < epsilon/2:
            A_flag = False
        else:
            now_x1 = gl.nextX2(newP,now_x1,now_x2)
            counter += 1

    #-- update class B--#
    if B_flag:
        dist = np.linalg.norm(now_x1 - now_x2)
        b_newX = pkl.dumps((now_x1,now_x2,'B'))
        for i in range(NODES):
            client[i].sendall(b'stepi')
            sign = gl.recvall(client[i])
            client[i].sendall(b_newX)
        #get newP
        newP_list = []
        PbarX_list = []
        for i in range(NODES):
            b_newP = gl.recvall(client[i])
            node_P,node_PbarX = pkl.loads(b_newP)
            newP_list.append(node_P)
            PbarX_list.append(node_PbarX)
        PbarX_list = np.array(PbarX_list)
        newP = newP_list[np.argmin(PbarX_list)] #choose min PbarX
        newPbarX = np.min(PbarX_list)
        now_x2 = gl.nextX2(newP,now_x2,now_x1)
        if 1 - newPbarX/dist < epsilon/2:
            B_flag = False
        counter += 1

end_time = dt.now().strftime('%s')
#--test output--#
DBS = gl.weight(now_x1,now_x2)
print('itr:',counter,'RMSE:',alg.RMSE(ANS_DBS_LIST[0][0],DBS))

#--end session--#
#send session ending command
for i in range(NODES):
    client[i].sendall(b'end')
