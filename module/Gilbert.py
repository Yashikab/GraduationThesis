import sys
sys.path.append('./module')
sys.path.append('./cpp_module')
import pandas as pd
import numpy as np
import socket

'''
This module is to calculate some part of the Gilbert Algorithm.
You have to add number of points in dataset in every function.
'''
#--index --#
columnlist = []
variable = []
dim = 2
for i in range(dim):
    v_name = 'x' + str(i)
    columnlist.append(v_name)
    variable.append(v_name)
columnlist.append('label') # 1 or -1

def vec_ab(a, b):
    return b - a

def minDistP(set_P):

    dist_list = [np.linalg.norm(p) for p in set_P]
    x1 = set_P[np.argmin(dist_list)]

    return x1


def PbarX(x, set_P):
    x_l2 = np.linalg.norm(x)
    PbarX_list = [np.dot(x,p)/x_l2 for p in set_P]
    minPbarX = np.min(PbarX_list)
    minP = set_P[np.argmin(PbarX_list)]

    return [minP, minPbarX]

def PbarX_Max(x1,x2, set_P):
    x2_x1 = x2 - x1
    x_l2 = np.linalg.norm(x2_x1)
    PbarX_list = [np.dot(x2_x1, p - x1) / x_l2 for p in set_P]
    # PbarX_list = np.dot(x2_x1,set_P - x1)/x_l2
    maxPbarX = np.max(PbarX_list)
    maxP = set_P[np.argmax(PbarX_list)]

    return [maxP, maxPbarX]

#x1: origin
def PbarX_Min(x1, x2, set_P):
    x2_x1 = x2 - x1
    x_l2 = np.linalg.norm(x2_x1)
    PbarX_list = [np.dot(x2_x1, p - x1) / x_l2 for p in set_P]
    minPbarX = np.min(PbarX_list)
    minP = set_P[np.argmin(PbarX_list)]
    # print(x_l2)

    return [minP,minPbarX]

def nextX(P, x):
    P = np.array(P)
    x = np.array(x)
    xp_dist = np.linalg.norm(P - x)
    unitXP = (P - x) / xp_dist
    xo = (-1) * x

    inner = np.dot(unitXP, xo)
    if inner < 0.0:
        thisX = x

    else:
        thisX_list = x + unitXP * inner
        thisX = pd.Series(thisX_list)

    return thisX

def nextX2(p, x1, x2):
    # print(p,x1,x2)
    p_x1 = p - x1
    x2_x1 = x2 - x1
    p_x1_L2 = np.linalg.norm(p_x1)
    unit_p_x1 = p_x1 / p_x1_L2
    inner = np.dot(unit_p_x1, x2_x1)
    if inner < 0.0:
        thisX = x1
    elif inner > p_x1_L2:
        thisX = p
    else:
        thisX = x1 + inner * unit_p_x1

    return thisX

MAX_SIZE = 4096
def recvall(sock):
    data = b''
    while True:
        part = sock.recv(MAX_SIZE)
        data += part
        if len(part) < MAX_SIZE:
            break
    return data


def weight(x1, x2):
    weight = x1 - x2
    bias = (-1) * np.dot(weight, (x1 + x2) / 2)
    DBS = np.append(weight,bias)
    return DBS

#--kikuchi Gilbert--#
def mutual_update(set_P, x_1, x_2, epsilon):
    dist = np.linalg.norm(x_1 - x_2)
    minP, minPbarX = PbarX_Min(x_2, x_1, set_P)
    next_x = nextX2(minP, x_1, x_2)
    if 1 - minPbarX / dist < epsilon / 2:
        return None
    return next_x
