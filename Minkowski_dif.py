import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle as pkl
import numpy as np
import pandas as pd

dim = 2
num = 50
#--index --#
columnlist = []
for i in range(dim):
    v_name = 'x' + str(i)
    columnlist.append(v_name)
#columnlist.append('label') # 1 or -1


#--load pickle--#
title = './datasets/pickle/2class_dataset'+ str(num) +'P_'+ str(dim) + 'dim.pkl'
with open(title,'rb') as f:
    dataset = pkl.load(f)



set_A = pd.DataFrame([],columns=(columnlist))
set_B = pd.DataFrame([],columns=(columnlist))

#-- separate with class--#
for i in range(len(dataset)):
	if dataset.loc[i,'label'] == 1:
		set_A = set_A.append(dataset.loc[i,columnlist],ignore_index=True)
	elif dataset.loc[i,'label'] == -1:
		set_B = set_B.append(dataset.loc[i,columnlist],ignore_index=True)

#--set base vector--#
BASE_VEC = [set_A.loc[0],set_B.loc[0]] #a0,b0

Minkowski = pd.DataFrame([],columns=(columnlist))
for a in range(len(set_A)):
	for b in range(len(set_B)):
		Minkowski = Minkowski.append(set_A.loc[a,columnlist] - set_B.loc[b,columnlist]
									,ignore_index=True)

    
'''
OUTPUT_PATH = './datasets/pickle/'
with open(OUTPUT_PATH+'Minkowski_'+ str(num) +'P_'+ str(dim) + 'dim.pkl','wb') as f:
	pkl.dump(Minkowski,f)
with open(OUTPUT_PATH+'Minkowski_base_vector.pkl','wb') as f:
	pkl.dump(BASE_VEC,f)
'''


#-- plot average --#
plt.scatter(Minkowski[columnlist[0]],Minkowski[columnlist[1]]
			,color = 'royalblue',marker='*',label='Minkowski')
plt.scatter(0,0,color='black',marker='o')

#--set Params--#
plt.legend()
plt.title(u'Minkowski')
plt.xlabel(u'x0')
plt.ylabel(u'x1')
plt.axes().set_aspect('equal','datalim')
plt.xlim([-2,12])
plt.ylim([0,10])

#--save png--#
OUTPUT_PATH = './image/Minkowski_50P.png'
plt.savefig(OUTPUT_PATH)