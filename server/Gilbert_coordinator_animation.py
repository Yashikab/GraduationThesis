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
#--initial definition--#
MAX_SIZE = 4096
DATA_PATH = '../datasets/'
DATA_NUM = 500 
EPSILON = 0.01
CONDITION = 10


#--address&port--#
HOST = 'localhost'
NODES = 3
PORT_LIST = []
for PORT in range(18400,18400+NODES):
    PORT_LIST.append(PORT)

#--for animation--#
P_from_node = [[] for i in range(NODES)]
choose_P = []
choose_x = []

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



#--load datasets--#
title = DATA_PATH + 'dataset' + str(DATA_NUM) + '_dist5.csv'
dataset = pd.read_csv(title)

#--devide origin&data--#
origin = dataset.loc[0,:]
data = pd.DataFrame(dataset[1:])
SET_NUM = len(data)
data = data.reset_index(drop=True)

#--get set P (separate for nodes)--#
EACH_SET = math.ceil(len(dataset) / NODES)
set_P = []
for i in range(0,SET_NUM,EACH_SET):
    if i+EACH_SET >= SET_NUM:
        node_data = pd.DataFrame(data[i:])
    else:
        node_data = pd.DataFrame(data[i:i+EACH_SET])
    node_data = node_data.reset_index(drop=True)
    set_P.append(node_data)

#--send dataset--#
b_data = []
for i in range(NODES):
    b_data.append(pkl.dumps(set_P[i])) # to binary data
    client[i].sendall(b'dataset') #protocol
for i in range(NODES):
    sign = gl.recvall(client[i])
    client[i].sendall(b_data[i]) # send data

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
    P_from_node[i].append([node_x1,0])

x1_L2_list = np.array(x1_L2_list) #choose minimum
x1 = x1_list[x1_L2_list.argmin()]
p1 = x1
choose_x.append(x1)



#--loop params--#
epsilon = EPSILON
cond = CONDITION
counter = 0
#--step i--#
newX = x1
newP = [p1,0]
choose_P.append(newP)
start_time = dt.now().strftime('%s')
while True:
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
        P_from_node[i].append(node_P)
    PbarX_list = np.array(PbarX_list)
    newP = newP_list[PbarX_list.argmin()] #choose min PbarX
    choose_P.append(newP)
    #check condition
    dist_X = np.linalg.norm(newX)
    cond = 1.0 - (newP[1]/dist_X)

    #calculate newX
    newX = gl.nextX(newP[0],newX)
    dist_newX = np.linalg.norm(newX)
    choose_x.append(newX)
    # less than epsilon
    if cond <= epsilon:
        #send session ending command
        #for i in range(NODES):
        #    client[i].sendall(b'end')
        break
    counter += 1
    #print('newX:%.3f\tnewP:%.3f' % (dist_newX,newP[1]))
end_time = dt.now().strftime('%s')
#--test output--#
total_time = int(end_time) - int(start_time)
print('Num: %d\tDist: %.3f\tIteration:%d\tTime:%dsec' % (DATA_NUM,dist_newX,counter,total_time))

#--output pickle for animation--#
PKL_PATH = '../result/pickle/Dist_ani/'
NAME_LIST = ['P_from_node.pkl','choose_x.pkl','choose_P.pkl']
DATA_LIST = [P_from_node,choose_x,choose_P]
for i in range(3):
	title = PKL_PATH + NAME_LIST[i]
	with open(title ,'wb') as f:
		pkl.dump(DATA_LIST[i],f)

#--end session--#
#send session ending command
for i in range(NODES):
    client[i].sendall(b'end')
