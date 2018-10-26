from numpy.random import *
import numpy as np
import pandas as pd

#--definition--#
d = 5
dim = 100
num_list = [5000]
count = 1
columnlist = []
for i in range(dim):
    v_name = 'x' + str(i)
    columnlist.append(v_name)

for num in num_list:    
    #--create dataframe--#
    dataset = pd.DataFrame([[0 for i in range(dim)]],columns=(columnlist))
    
    #--length to O is more than d--#
    while(True):
        if count > num:
            print('exit')
            break
        else:        
            #--create randam variable (1,2) --#
            x = rand(dim)
            x2 = 0.
            for i in range(dim):
                x2 += np.square(x[i])

        
            dist = np.sqrt(x2)
        
            if(dist >= d):
                newvar = pd.DataFrame([x],columns=(columnlist))
                dataset = dataset.append(newvar,ignore_index=True)
                count +=1

            dataset.to_csv('dataset'+ str(num) +'_dist5_'+ str(dim) + 'dim.csv',index=False)


