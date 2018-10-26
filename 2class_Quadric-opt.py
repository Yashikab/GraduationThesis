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
DATA_NUM = 50
DIM = 2
#--import sample point set --#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim.pkl'
with open(title,'rb') as f:
    dataset = pkl.load(f)
dataset = np.array(dataset)
columnlist = []
variable = []
for i in range(DIM):
    columnlist.append('x' + str(i))
    variable.append('x'+ str(i))
columnlist.append('label') # 1 or -1
#--set origin--#
origin = [0 for i in range(DIM)]
set_num = len(dataset)
train_matrix = [[(-1)*p[2]*p[0],(-1)*p[2]*p[1],(-1)*p[2]] for p in dataset]
restrict = [-1.0 for i in range(set_num)]

#--set matrix--#
P = matrix(np.diag([2.0,2.0,0.0]))
q = matrix(np.array([0.0,0.0,0.0]))
G = matrix(np.array(train_matrix))
h = matrix(np.array(restrict))
#-- optimize --#
sol = co.solvers.qp(P,q,G,h)

#--calc distans (O,polytope)--#
print(sol['x'])
#--Graph output--#
x_data = [d[0] for d in dataset]
y_data = [d[1] for d in dataset]

plt.scatter(x_data,y_data,label='dataset')
x = np.arange(0,10,0.01)
y = (-1)*(sol['x'][0]*x + sol['x'][2])/sol['x'][1]
with open('./result/pickle/QP_2classDB.pkl','wb') as f:
	pkl.dump([x,y],f)
plt.plot(x,y,label='Q-opt')
#plt.scatter(2*thisX['X'],2*thisX['Y'],label='QP')
plt.savefig('QP_2class.png')
#plt.show()
