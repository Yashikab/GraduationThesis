import sys
sys.path.append('./module')

import Gilbert as gl
import pandas as pd
import numpy as np
from datetime import datetime as dt
from tqdm import tqdm
import pickle
from joblib import Parallel, delayed


#--definition--#
EPSILON = 0.01
CONDITION = 10
num_list = [300,500,700,1000,3000,5000,7000,10000,30000]
dim = 10
experiment_num = 100
columnlist = []
for i in range(dim):
    columnlist.append('x' + str(i))

#--time result--#
time_result = pd.DataFrame()
time_outline = []
for num in num_list:
    #--import sample point set --#
    title = './datasets/dataset'+ str(num) +'_dist5_'+ str(dim) + 'dim.csv'
    dataset = pd.read_csv(title)

    #--set origin--#
    origin = dataset.loc[0,:]

    #--get set P --#
    set_num = len(dataset)
    set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)
    set_P = set_P.reset_index(drop=True)

    #-- loop --#
    #step 1#
    #--calculate Minimum distance--#
    x1 = gl.minDistP(set_P)
    p1 = x1

    #step i#
    epsilon = EPSILON
    cond = CONDITION

    time_outline = []
    time_columns = ['NUM']
    def process(e_num):

        newX = x1
        newP = [p1,0]
        i = 0
        total_time = 0
        while True:
            #calc time
            start_time = dt.now().strftime('%s')

            newP = gl.PbarX(newX,set_P)

            #--check condition--#
            dist_X = np.linalg.norm(newX)
            cond = 1.0 - (newP[1]/dist_X)

            #--calc nextX--#
            newX = gl.nextX(newP[0],newX)
            dist_newX = np.linalg.norm(newX)

            # less than epsilon
            if cond <= epsilon:
                break

            i += 1

            end_time = dt.now().strftime('%s')

            total_time += int(end_time) - int(start_time)

        #--calc time--#
        avg_time = total_time / (i + 1)
        return avg_time

    time_outline = Parallel(n_jobs=-1,verbose=10)(delayed(process)(i) for i in range(experiment_num))
    #time_outline = one_outline
    title = './result/pickle/result_Ordinal_' + str(num) + 'P.pkl'
    with open(title,'wb') as f:
        pickle.dump(time_outline,f)




