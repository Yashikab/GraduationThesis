from numpy.random import *
import numpy as np
import pandas as pd

#--definition--#
d = 5
num = 1000
count = 1

#--create dataframe--#
dataset = pd.DataFrame([[0,0]],columns=(list('XY')))

#--length to O is more than d--#
while(True):
    if count > num:
        print('exit')
        break
    else:
        
        #--create randam variable (1,2) --#
        x = rand(2)*10
        dist = np.sqrt(x[0]*x[0]+x[1]*x[1])
        
        if(dist >= d):
            newvar = pd.DataFrame([x],columns=(list('XY')))
            dataset = dataset.append(newvar,ignore_index=True)
            count +=1

dataset.to_csv('dataset1000_dist5.csv',index=False)
            

