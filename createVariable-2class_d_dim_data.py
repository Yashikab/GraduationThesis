from numpy.random import *
from numpy import *
import numpy as np
import pandas as pd
import pickle as pkl
import math
from tqdm import tqdm

PATH = './datasets/'
# with open(PATH+'ORIGINAL_DBS_' + str(DIM) + 'dim.pkl','wb') as f:
# 	pkl.dump(DBS,f)

DIM = 10
num = 10000#each class
bias = np.array([1] + [-1 for i in range(DIM-1)])
columnlist = []
for i in range(DIM):
    v_name = 'x' + str(i)
    columnlist.append(v_name)
columnlist.append('label') # 1 or -1

for i in range(5):
    #--Desicion boundary surface--#
    #d = 1
    MARGIN_list = [0.1,0.2,0.3]
    for MARGIN in MARGIN_list:
        p1 = np.array(rand(DIM)*0.2 + 0.4) #[x,y]
        p2 = np.array(rand(DIM)*0.2 + 0.4)
        dir_vec = p2 - p1
        son = 1
        for el in dir_vec:
            son *= el
        weight = son/dir_vec*bias
        DBS = np.append(weight,np.dot((-1)*weight,p1))
        print(DBS)
        #--initialize--#
        count_A = 1
        count_B = 1
        count = 1
        #--create dataframe--#
        dataset = pd.DataFrame([],columns=(columnlist))
        #--length to O is more than d--#
        pbar = tqdm(total=num*2)
        while(True):
            if count_A > num and count_B > num:
                print('Done')
                break
            else:        
                #--create randam variable (1,2) --#
                x = rand(DIM)
                x_b = np.append(x,1)
                Subst = np.dot(DBS,x_b)
                DBS_w = np.array([DBS[p] for p in range(DIM)])
                dist = math.fabs(Subst)/np.linalg.norm(DBS_w)
                if dist >= MARGIN:
                    if Subst > 0 and count_A <=num:
                        x = np.append(x,1)
                        newvar = pd.DataFrame([x],columns=(columnlist))
                        dataset = dataset.append(newvar,ignore_index=True)
                        count_A += 1
                        pbar.update(1)
                    elif Subst < 0 and count_B <=num:
                        x = np.append(x,-1)
                        newvar = pd.DataFrame([x],columns=(columnlist))
                        dataset = dataset.append(newvar,ignore_index=True)
                        count_B += 1
                        pbar.update(1)
        pbar.close()    
                    
        dataset.to_csv(PATH+'2class_dataset'+ str(num) +'P_'+ str(DIM)
                         + 'dim_' + str(MARGIN) + 'M_' + str(i) + '.csv',index=False)


