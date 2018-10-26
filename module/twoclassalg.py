import sys
sys.path.append('../cpp_module')
import pandas as pd
import numpy as np
import Gilbert as gl
from datetime import datetime as dt
import pickle as pkl
#import cvxopt as co
#from cvxopt import matrix
from tqdm import tqdm
import math
import socket
import time
import basic
#--common definition--#
cond = 10

def coresets(EPSILON, set_A, set_B):
    basic.inputdata(set_A.tolist(), set_B.tolist())
    start_time = time.time()
    #step 1#
    x_1i = np.array(set_A[0])
    x_2i = np.array(set_B[0])
    #-- loop --#
    epsilon = EPSILON
    itr = 0
    pbar = tqdm()
    while True:
        #step i#
        #p_1i,g_1i = gl.PbarX_Max(x_1i,x_2i,set_A)
        PbarX_list1 = basic.dotlist(x_1i.tolist(), x_2i.tolist(),0)
        g_1i = np.max(PbarX_list1)
        p_1i = set_A[np.argmax(PbarX_list1)]

        #p_2i,g_2i = gl.PbarX_Max(x_2i,x_1i,set_B)
        PbarX_list2 = basic.dotlist(x_2i.tolist(), x_1i.tolist(),1)
        g_2i = np.max(PbarX_list2)
        p_2i = set_B[np.argmax(PbarX_list2)]

        f_i = np.linalg.norm(x_1i - x_2i)
        mother1 = max(np.linalg.norm(x_1i - p_1i), np.sqrt(g_1i * f_i))
        mother2 = max(np.linalg.norm(x_2i - p_2i), np.sqrt(g_2i * f_i))
        if mother1 != 0:
            ratio1 = g_1i / mother1
        else:
            ratio1 = 0
        if mother2 != 0:
            ratio2 = g_2i / mother2
        else:
            ratio2 = 0

        cond = 1 - (f_i - (g_1i + g_2i)) / f_i
        if ratio1 > ratio2:
            #update 1
            x_1i = gl.nextX2(p_1i, x_1i, x_2i)
        else:
            #update 2
            x_2i = gl.nextX2(p_2i, x_2i, x_1i)
        # print('Dist: %.3f\tCondition: %.3f' % (f_i,cond))
        if cond <= epsilon:
        # if i > 5:
            break
        itr += 1
        pbar.update()
    end_time = time.time()
    pbar.close()
    DBS = gl.weight(x_1i, x_2i)
    print('coresets done!')
    return (DBS, itr, end_time - start_time)

def kikuchi(EPSILON, set_A, set_B):
    basic.inputdata(set_A.tolist(), set_B.tolist())
    start_time = time.time()
    x1 = set_A[0]
    dist_list = [np.linalg.norm(x1 - x) for x in set_B]
    x2 = set_B[np.argmin(dist_list)]
    A_flag = True
    B_flag = True
    itr = 0
    pbar = tqdm()
    while(A_flag or B_flag):
        if A_flag:
            # update
            # update = gl.mutual_update(set_A, x1, x2, EPSILON)
            dist = np.linalg.norm(x1 - x2)
            PbarX_list = basic.dotlist(x2.tolist(), x1.tolist(),0)
            minPbarX = np.min(PbarX_list)
            minP = set_A[np.argmin(PbarX_list)]
            next_x = gl.nextX2(minP, x1, x2)
            if 1 - minPbarX / dist < EPSILON / 2:
                update = None
            else:
                update = next_x

            if not isinstance(update, np.ndarray):
                A_flag = False
            else:
                x1 = update
                itr += 1
                pbar.update(1)
        if B_flag:
            # update = gl.mutual_update(set_B, x2, x1, EPSILON)
            dist = np.linalg.norm(x2 - x1)
            PbarX_list = basic.dotlist(x1.tolist(), x2.tolist(),1)
            minPbarX = np.min(PbarX_list)
            minP = set_B[np.argmin(PbarX_list)]
            next_x = gl.nextX2(minP, x2, x1)
            if 1 - minPbarX / dist < EPSILON / 2:
                update = None
            else:
                update = next_x


            if not isinstance(update, np.ndarray):
                B_flag = False
            else:
                x2 = update
                itr += 1
                pbar.update(1)
    end_time = time.time()
    pbar.close()
    DBS = gl.weight(x1, x2)
    print('kikuchi done!')
    return (DBS, itr, end_time - start_time)

# def quadratic(dataset,DIM):
#     set_num = len(dataset)
#     train_matrix = [[(-1)*data[DIM]*data[d] for d in range(DIM)] + [(-1)*data[DIM]] for data in dataset]
#     restrict = [-1.0 for i in range(set_num)]

#     #--set matrix--#
#     P = matrix(np.diag([1.0 for d in range(DIM)] + [0.0]))
#     q = matrix(np.array([0.0 for d in range(DIM+1)]))
#     G = matrix(np.array(train_matrix))
#     h = matrix(np.array(restrict))
#     #-- optimize --#
#     sol = co.solvers.qp(P,q,G,h)
#     DBS = np.array([p for p in sol['x']])
#     print('QP done!')
#     return DBS

def dist_kikuchi(EPSILON,data,DIM):
    #--address&port--#
    MAX_SIZE = 4096
    HOST = 'localhost'
    NODES = 6
    PORT_LIST = []
    for PORT in range(18400, 18400 + NODES):
        PORT_LIST.append(PORT)

    #--access to each server--#
    address = []
    client = []
    for PORT in PORT_LIST:
        address.append((HOST, PORT))
        client.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    for i in range(NODES):
        client[i].connect(address[i])
        client[i].sendall(b'2class')
        log = client[i].recv(MAX_SIZE)


    #--devide origin&data--#
    SET_NUM = len(data)

    #--get set P (separate for nodes)--#
    set_P = [[] for i in range(NODES)]
    for i in range(SET_NUM):
        set_P[i % NODES].append(data[i])


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
    start_time = time.time()
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
        L2 = np.linalg.norm(node_x21 - x11)
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
    pbar = tqdm()
    while (A_flag or B_flag):

        #-- update class A--#
        if A_flag:
            dist = np.linalg.norm(now_x1 - now_x2)
            b_newX = pkl.dumps((now_x1, now_x2, 'A'))
            for i in range(NODES):
                client[i].sendall(b'stepi')
                sign = gl.recvall(client[i])
                client[i].sendall(b_newX)
            #get newP
            newP_list = []
            PbarX_list = []
            for i in range(NODES):
                b_newP = gl.recvall(client[i])
                node_P, node_PbarX = pkl.loads(b_newP)
                newP_list.append(node_P)
                PbarX_list.append(node_PbarX)
            PbarX_list = np.array(PbarX_list)
            newP = newP_list[np.argmin(PbarX_list)] #choose min PbarX
            newPbarX = np.min(PbarX_list)

            if 1 - newPbarX / dist < epsilon / 2:
                A_flag = False
            else:
                now_x1 = gl.nextX2(newP, now_x1, now_x2)
                counter += 1
                pbar.update(1)
        #-- update class B--#
        if B_flag:
            dist = np.linalg.norm(now_x1 - now_x2)
            b_newX = pkl.dumps((now_x1, now_x2, 'B'))
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
            if 1 - newPbarX / dist < epsilon / 2:
                B_flag = False
            else:
                now_x2 = gl.nextX2(newP, now_x2, now_x1)
                counter += 1
                pbar.update(1)

    end_time = time.time()
    pbar.close()
    #--test output--#
    DBS = gl.weight(now_x1, now_x2)
    #--end session--#
    #send session ending command
    for i in range(NODES):
        client[i].sendall(b'end')
    print('Dist_kikuchi Done!')
    return (DBS, counter, end_time - start_time)


def RMSE(ans_DBS,pred_DBS):
     return np.sqrt(sum([np.square(ans_DBS[p] - pred_DBS[p]) for p in range(len(pred_DBS))])/len(pred_DBS))

def ckcorrect(set_A,set_B,DBS):
    correct = 0
    incorrect = 0

    for i in range(len(set_A)):
        if np.dot(np.append(set_A[i], 1), DBS) > 0:
            correct += 1
        else:
            incorrect += 1
    for i in range(len(set_B)):
        if np.dot(np.append(set_B[i], 1), DBS) < 0:
            correct += 1
        else:
            incorrect += 1
    return correct
