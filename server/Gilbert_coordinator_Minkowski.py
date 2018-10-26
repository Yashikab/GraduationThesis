import sys
sys.path.append('../module')
import socket
from datetime import datetime as dt
import pickle as pkl
import Gilbert as gl
import Minkowski as mks
import pandas as pd
import numpy as np
import math
import time

#--initial definition--#
MAX_SIZE = 4096
DATA_PATH = '../datasets/pickle/'
DATA_NUM = 50
DIM = 2
EPSILON = 0.01
CONDITION = 10


#--address&port--#
HOST = 'localhost'
NODES = 10
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

#--load 2-class datasets--#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim.pkl'
with open(title,'rb') as f:
    Original_dataset = pkl.load(f)

#--calc Minkowski difference--#
dataset,Original_A,Original_B = mks.difference(DIM,Original_dataset)

#--devide origin&data--#
origin = [0 for i in range(DIM)]
data = pd.DataFrame(dataset[0:])
data = np.array(data)
SET_NUM = len(data)
#data = data.reset_index(drop=True)

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
counter = 0
#--step i--#
newX = x1
newP = [p1,0]

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

#--end session--#
#send session ending command
for i in range(NODES):
    client[i].sendall(b'end')

#--calc decision boundary surface--#
weight = np.array(newX)


#--search support vector--#
'''
for i in range(len(dataset)):
	if np.array(newP) == np.array(dataset.loc[i,:]):
		break
vec_a = np.array(Original_A.loc[i,:])
vec_b = np.array(Original_B.loc[i,:])
'''
SVa = mks.search_sv(Original_A,weight,True)
SVb = mks.search_sv(Original_B,weight,False)
#ans_vec = SV + (-1)*dist_X/2
b1 = np.dot(weight,SVa)
b2 = np.dot(weight,SVb)
DBS_b = (-1)*(b1+b2)/2

DBS = np.append(weight,DBS_b)

print(DBS)

OUTPUT = '../result/pickle/New_DBS.pkl'
with open(OUTPUT,'wb') as f:
    pkl.dump(DBS,f)
