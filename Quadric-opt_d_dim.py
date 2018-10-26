import pandas as pd
import numpy as np
import cvxopt as co
from cvxopt import matrix
#import matplotlib.pyplot as plt

#--definition--#
dim = 10
NUM_LIST = [1000,5000,10000]
columnlist = []
for i in range(dim):
    columnlist.append('x' + str(i))


for num in NUM_LIST:
    #--import sample point set --#
    dataset = pd.read_csv('./datasets/dataset'+str(num)+'_dist5_'+str(dim)+'dim.csv')

    #--set origin--#
    origin = list(dataset.loc[0,:])

    #--get set P --#
    set_num = len(dataset)
    set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)



    train_matrix = []
    restrict = []
    for i in range(set_num):
        if i == 0:
            row = origin + [1.0]
        else:
            set_P_list = []
            for ind in columnlist:
                set_P_list.append((-1)*set_P.loc[i,ind])

            row = set_P_list + [-1.0]
        train_matrix.append(row)
        restrict.append(-1.0)

    #--set matrix--#
    P_list = [2.0 for i in range(dim)]
    P = matrix(np.diag(P_list + [0.0]))
    q = matrix(np.array([0.0 for i in range(dim+1)]))
    G = matrix(np.array(train_matrix))
    h = matrix(np.array(restrict))
    #-- optimize --#
    sol = co.solvers.qp(P,q,G,h)

    #--calc distance (O,polytope)--#
    w_list = []
    for j in range(dim):
        w_list.append(sol['x'][j])
    w = pd.Series(w_list,index=columnlist)
    w_l2 = np.linalg.norm(w)

    
    dist_X = 2*np.absolute((-1)*sol['x'][dim])/w_l2

    print('Dist: %.3f' % dist_X)

    
