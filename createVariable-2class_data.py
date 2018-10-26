from numpy.random import *
import numpy as np
import pandas as pd
import pickle as pkl
import math

#--definition--#
d = 0
DBS_w = [1,1] #[x,y]
DBS_b = -10 #-b

dim = 2
num_list = [50] #each class
count_A = 1
count_B = 1
count = 1
columnlist = []
for i in range(dim):
    v_name = 'x' + str(i)
    columnlist.append(v_name)
columnlist.append('label') # 1 or -1

OUTPUT_PATH = './datasets/pickle/'

for num in num_list:    
    #--create dataframe--#
    dataset = pd.DataFrame([],columns=(columnlist))
    
    #--length to O is more than d--#
    while(True):
        if count_A > num and count_B > num:
            print('exit')
            break
        else:        
            #--create randam variable (1,2) --#
            x = rand(dim)*10
            Subst = np.dot(DBS_w,x) + DBS_b

            dist = math.fabs(Subst)/np.linalg.norm(DBS_w)       
            if(dist >= d):
                if Subst > 0 and count_A <=num:
                    x = np.append(x,1)
                    newvar = pd.DataFrame([x],columns=(columnlist))
                    dataset = dataset.append(newvar,ignore_index=True)
                    count_A += 1
                elif Subst < 0 and count_B <=num:
                    x = np.append(x,-1)
                    newvar = pd.DataFrame([x],columns=(columnlist))
                    dataset = dataset.append(newvar,ignore_index=True)
                    count_B += 1

                
    with open(OUTPUT_PATH+'NEW2class_dataset'+ str(num) +'P_'+ str(dim) + 'dim.pkl','wb') as f:
        pkl.dump(dataset,f)


