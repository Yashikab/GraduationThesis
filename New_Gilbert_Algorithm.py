#--add PATH to selfmodule--#
import sys
sys.path.append('./module')

import pandas as pd
import numpy as np
import Gilbert as gl
from datetime import datetime as dt
import pickle as pkl

#--definition--#
EPSILON = 0.01
num_list = [5000,10000,30000]
dim = 10
columnlist = []
for i in range(dim):
    columnlist.append('x' + str(i))

#--time result--#
time_result = pd.DataFrame()
start_time = dt.now().strftime('%s')

for num in num_list:
    #--import sample point set --#
    title = './datasets/dataset'+ str(num) +'_dist5_'+str(dim)+'dim.csv'
    dataset = pd.read_csv(title)

    #--set origin--#
    #origin = dataset.loc[0,:]

    #--get set P --#
    set_num = len(dataset)
    set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)
    set_P = set_P.reset_index(drop=True)
    set_P = np.array(set_P)
   #-- loop --#
    epsilon = EPSILON
    cond = 10
    i = 0

    #step 1#   
    x1 = gl.minDistP(set_P)
    p1 = x1

    allX = []
    allP = []
    #step i#
    newX = x1
    newP = [p1,0]

    allX.append(newX)
    allP.append(newP)

    start_time = dt.now().strftime('%s')
    while True:
        newP = gl.PbarX(newX,set_P)

        #--check condition--#
        dist_X = np.linalg.norm(newX)
        cond = 1.0 - (newP[1]/dist_X)

        newX = gl.nextX(newP[0],newX)
        dist_newX = np.linalg.norm(newX)


        allX.append(newX)
        allP.append(newP)

        # less than epsilon
        if cond <= epsilon:
            break

        i += 1
    end_time = dt.now().strftime('%s')
    total_time = int(end_time) - int(start_time)
    print('Dist: %.3f\tIteration:%d\tTime:%dsec' % (dist_newX,i,total_time))

    # with open('./result/pickle/Ordinal_ani/allP.pkl','wb') as f:
    # 	pkl.dump(allP,f)
    # with open('./result/pickle/Ordinal_ani/allX.pkl','wb') as f:
    # 	pkl.dump(allX,f)


