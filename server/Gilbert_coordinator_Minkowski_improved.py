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
    client[i].sendall(b'2class')
    log = client[i].recv(MAX_SIZE)

#--load 2-class datasets--#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim.pkl'
with open(title,'rb') as f:
    Original_dataset = pkl.load(f)

#--index --#
columnlist = []
variable =[]
for i in range(DIM):
    v_name = 'x' + str(i)
    columnlist.append(v_name)
    variable.append(v_name)
columnlist.append('label') # 1 or -1
#--devide origin&data--#
origin = [0 for i in range(DIM)]


#--get set P (separate for nodes)--#
set_P = [pd.DataFrame([],columns=(columnlist)) for i in range(NODES)]
for i in range(len(Original_dataset)):
    #print(Original_dataset.loc[i])
    #print(type(Original_dataset.loc[i]))
    set_P[i%NODES] = set_P[i%NODES].append(Original_dataset.loc[i],ignore_index=True)

for i in range(NODES):
    set_P[i].reset_index(drop=True)
    #print(set_P[i])


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
for i in range(len(Original_dataset)):
    if Original_dataset.loc[i,'label'] == 1:
        x_a = Original_dataset.loc[i,variable]
for i in range(len(Original_dataset)):
    if Original_dataset.loc[i,'label'] == -1:
        x_b = Original_dataset.loc[i,variable]

#--loop params--#
epsilon = EPSILON
cond = CONDITION
counter = 0
#--step i--#
newx_a = np.array(x_a)
newx_b = np.array(x_b)
newX = newx_a - newx_b
vec_newX = [newx_a,newx_b]
#newP = [p1,0]

start_time = dt.now().strftime('%s')
while True:
    
    #send x
    b_newX = pkl.dumps(vec_newX)
    for i in range(NODES):
        client[i].sendall(b'stepi')
        sign = gl.recvall(client[i])
        client[i].sendall(b_newX)

    #get newP
    anewP_list = []
    bnewP_list = []
    aPbarX_list = []
    bPbarX_list = []
    for i in range(NODES):
        b_newP = gl.recvall(client[i])
        node_P = pkl.loads(b_newP)
        anewP_list.append(node_P[0])
        bnewP_list.append(node_P[1])
        aPbarX_list.append(node_P[0][1])
        bPbarX_list.append(node_P[1][1])

    aPbarX_list = np.array(aPbarX_list)
    bPbarX_list = np.array(bPbarX_list)
    anewP = anewP_list[aPbarX_list.argmin()] #choose min PbarX
    bnewP = anewP_list[bPbarX_list.argmax()] #choose min PbarX
    
    #check condition
    dist_X = np.linalg.norm(newX)
    cond = 1.0 - ((anewP[1]-bnewP[1])/dist_X)

    #calculate newX
    #ratio
    #print(anewP[1],np.linalg.norm(newX))
    ar = (np.linalg.norm(newX)-anewP[1])/max(np.linalg.norm(newx_a-anewP[0]),np.sqrt((np.linalg.norm(newX)-anewP[1])*(np.linalg.norm(newX))))
    br = (bnewP[1])/max(np.linalg.norm(newx_b-bnewP[0]),np.sqrt(bnewP[1]*(np.linalg.norm(newX))))
    if ar > br :
        newx_a = gl.nextX2(anewP[0],newx_a,newx_b)
        #print(newx_a)
    else:
        newx_b = gl.nextX2(bnewP[0],newx_b,newx_a)
    #print(newx_b)
    newX = newx_a - newx_b
    vec_newX = [newx_a,newx_b]
    #print(newX)
    dist_newX = np.linalg.norm(newX)
    print(dist_newX,cond)
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
#SVa = mks.search_sv(Original_A,weight,True)
#SVb = mks.search_sv(Original_B,weight,False)
#ans_vec = SV + (-1)*dist_X/2
#b1 = np.dot(weight,SVa)
#b2 = np.dot(weight,SVb)
#DBS_b = (-1)*(b1+b2)/2

#DBS = np.append(weight,DBS_b)

print(weight)

#OUTPUT = '../result/pickle/Improved_DBS.pkl'
#with open(OUTPUT,'wb') as f:
#    pkl.dump(DBS,f)
