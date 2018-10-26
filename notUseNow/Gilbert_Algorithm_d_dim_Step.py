import pandas as pd
import numpy as np
from datetime import datetime as dt
from tqdm import tqdm
import pickle
from joblib import Parallel, delayed


#--definition--#

num_list = [10,50,100,500,1000,5000,10000]
dim = 10
experiment_num = 100
columnlist = []
for i in range(dim):
    columnlist.append('x' + str(i))

#--time result--#
time_result = pd.DataFrame()
time_outline = []
def process(num):
    #--import sample point set --#
    title = './datasets/dataset'+ str(num) +'_dist5_'+ str(dim) + 'dim.csv'
    dataset = pd.read_csv(title)

    #--set origin--#
    origin = dataset.loc[0,:]

    #--get set P --#
    set_num = len(dataset)
    set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)


    #step 1#
    #--calculate Minimum distance--#
    for i in range(1,set_num):

        dist = np.linalg.norm(set_P.loc[i,:])

        if i == 1:
            min_dist = dist
            x1 = set_P.loc[i,:]
        elif min_dist > dist:
            min_dist = dist
            x1 = set_P.loc[i,:]
    p1 = x1


    #step i#
    #--calculate min p|x--#
    def calcminPbarX(x):
        for i in range(1,set_num):

            inner_px = np.dot(set_P.loc[i,:],x)
            x_l2 = np.linalg.norm(x)
            PbarX = inner_px/x_l2


            if i == 1:
                minPbarX = PbarX
                minP = set_P.loc[i,:]
            elif minPbarX > PbarX:
                minPbarX = PbarX
                minP = set_P.loc[i,:]

        return [minP,minPbarX]

    #-- minimum distant on line segment(x,newp)--#
    def calcNextX(P,x):

        P = np.array(P)
        x = np.array(x)
        xp_dist = np.linalg.norm(P - x)
        unitXP = (P - x)/xp_dist
        xo = (-1) * x

        inner = np.dot(unitXP,xo)

        if inner < 0.0:
            thisX = x
            msg = 'ok'
        else:
            thisX_list = x + unitXP*inner
            thisX = pd.Series(thisX_list,index=columnlist)

        return thisX
    result = pd.DataFrame()

    #-- loop --#
    epsilon = 0.01
    cond = 10



    newX = x1

    newP = [p1,0]
    i = 0
    step = 0;
    while True:

        newP = calcminPbarX(newX)

        #calc 1-epsilon approximation

        dist_X = np.linalg.norm(newX)
        cond = 1.0 - (newP[1]/dist_X)

        newX = calcNextX(newP[0],newX)

        dist_newX = np.linalg.norm(newX)


        # less than epsilon
        if cond <= epsilon:
            step = i
            break

        i += 1



    title = './result/pickle/result_Step_' + str(num) + 'P.pkl'
    with open(title,'wb') as f:
        pickle.dump(step,f)

Parallel(n_jobs=-1,verbose=1)(delayed(process)(i) for i in num_list)
