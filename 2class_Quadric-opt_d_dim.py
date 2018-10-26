import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import cvxopt as co
from cvxopt import matrix
import matplotlib.pyplot as plt
import pickle as pkl
#--import sample point set --#
DATA_PATH = './datasets/pickle/'
DATA_NUM = 10000
DIM = 10
#--import sample point set --#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim.pkl'
with open(title,'rb') as f:
    dataset = pkl.load(f)
dataset = np.array(dataset)

#--set origin--#
origin = [0 for i in range(DIM)]
set_num = len(dataset)
train_matrix = [[(-1)*data[DIM]*data[d] for d in range(DIM)] + [(-1)*data[DIM]] for data in dataset]
restrict = [-1.0 for i in range(set_num)]

#--set matrix--#
P = matrix(np.diag([1.0 for d in range(DIM)] + [0.0]))
q = matrix(np.array([0.0 for d in range(DIM+1)]))
G = matrix(np.array(train_matrix))
h = matrix(np.array(restrict))
#-- optimize --#
sol = co.solvers.qp(P,q,G,h)

#--calc distans (O,polytope)--#
print(np.array(sol['x']/sol['x'][0]))
