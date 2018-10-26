import sys
sys.path.append('./module')

import numpy as np
import pandas as pd
import Gilbert as gl
import pickle as pkl


DATA_PATH = './datasets/pickle/'
DATA_NUM = 10000
DIM = 10
#--import sample point set --#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim.pkl'
with open(title,'rb') as f:
    Original_dataset = pkl.load(f)


#--devide origin&data--#
origin = [0 for i in range(DIM)]
dataset =np.array(Original_dataset)
SET_NUM = len(dataset)

set_A = []
set_B = []

#-- separate with class--#
for data in dataset:
	if data[DIM] == 1:
		set_A.append([data[d] for d in range(DIM)])
	elif data[DIM] == -1:
		set_B.append([data[d] for d in range(DIM)])

set_A = np.array(set_A)
set_B = np.array(set_B)

#--import weight--#
with open('./result/pickle/kikuchi_weight.pkl','rb') as f:
	DBS = pkl.load(f)
DBS = np.array(DBS)
correct = 0
incorrect = 0

for i in range(len(set_A)):
	if np.dot(np.append(set_A[i],1),DBS) > 0:
		correct += 1
	else:
		incorrect += 1
for i in range(len(set_B)):
	if np.dot(np.append(set_B[i],1),DBS) < 0:
		correct += 1
	else:
		incorrect += 1
print('Total:',SET_NUM,'Correct:',correct,'Incorrect',incorrect)