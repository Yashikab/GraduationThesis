import sys
sys.path.append('./module')
import pandas as pd
import numpy as np
import Gilbert as gl
import pickle as pkl
from tqdm import tqdm
from datetime import datetime as dt
import math
import socket
import time

def coresets(EPSILON,set_A,set_B):
    start_time = time.time()
    #step 1#
    x_1i = np.array(set_A[0])
    x_2i = np.array(set_B[0])
    #-- loop --#
    epsilon = EPSILON
    itr = 0
    pbar = tqdm(total=10000)
    while True:
        #step i#
        p_1i,g_1i = gl.PbarX_Max(x_1i,x_2i,set_A)
        p_2i,g_2i = gl.PbarX_Max(x_2i,x_1i,set_B)
        f_i = np.linalg.norm(x_1i-x_2i)
        mother1 = max(np.linalg.norm(x_1i - p_1i),np.sqrt(g_1i*f_i))
        mother2 = max(np.linalg.norm(x_2i - p_2i),np.sqrt(g_2i*f_i))
        if mother1 != 0:
            ratio1 = g_1i/mother1
        else:
            ratio1 = 0
        if mother2 != 0:
            ratio2 = g_2i/mother2
        else:
            ratio2 = 0

        cond = 1 - (f_i-(g_1i+g_2i))/f_i
        if ratio1 > ratio2:
            #update 1
            x_1i = gl.nextX2(p_1i,x_1i,x_2i)
        else:
            #update 2
            x_2i = gl.nextX2(p_2i,x_2i,x_1i)
        #print('Dist: %.3f\tCondition: %.3f' % (f_i,cond))
        if cond <= epsilon:
        #if i > 5:
            break
        itr += 1
        pbar.update(1)
    end_time = time.time()
    pbar.close()
    DBS = gl.weight(x_1i,x_2i)
    print('coresets done!')
    return (DBS,itr,end_time-start_time)

#--read file--#
DATA_NUM = 1
DATA_PATH = './datasets/pickle/2class_d/'
DIM = 10
NUM = 10000
MARGIN_LIST = [0.2]
DATASET_LIST = [[] for i in range(DATA_NUM)]

for i in range(DATA_NUM):
    for m in MARGIN_LIST:
        title = DATA_PATH + '2class_dataset' + str(NUM) + 'P_' + str(DIM) + 'dim_' + str(m) + 'M_' + str(i) + '.pkl'
        #dataset = pd.read_csv(title)
        with open(title,'rb') as f:
            dataset,ans = pkl.load(f)
        DATASET_LIST[i].append(np.array(dataset))

CORE_DBS = [[] for i in range(DATA_NUM)]
CORE_itr = [[] for i in range(DATA_NUM)]
CORE_time = [[] for i in range(DATA_NUM)]

#--run Algorithms--#
EPSILON = 0.01
for i in range(DATA_NUM):
    for m in range(len(MARGIN_LIST)):
        #--separate class--#
        set_A = []
        set_B = []
        for data in DATASET_LIST[i][m]:
            if data[DIM] == 1:
                set_A.append([data[d] for d in range(DIM)])
            elif data[DIM] == -1:
                set_B.append([data[d] for d in range(DIM)])
        set_A = np.array(set_A)
        set_B = np.array(set_B)


        c_DBS,c_itr,c_time = coresets(EPSILON,set_A,set_B)

        CORE_DBS[i].append(c_DBS/np.max(np.abs(c_DBS)))
        CORE_itr[i].append(c_itr)
        CORE_time[i].append(c_time)

# with open('./result/pickle/evaluation.pkl','wb') as f:
#     pkl.dump((QP_DBS,CORE_DBS,CORE_itr,KIKU_DBS,KIKU_itr),f)