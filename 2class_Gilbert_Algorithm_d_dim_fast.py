import sys
sys.path.append('./module')
import pandas as pd
import numpy as np
import Gilbert as gl
#import matplotlib.pyplot as plt
from datetime import datetime as dt
import pickle as pkl

#--initial definition--# 
DATA_PATH = './datasets/pickle/2class_d/'
DATA_NUM = 1000
DIM = 10
EPSILON = 0.01
CONDITION = 10

MARGIN = 0.3
i = 3
#--import sample point set --#
title = DATA_PATH + '2class_dataset'+ str(DATA_NUM) +'P_'+ str(DIM) + 'dim_' + str(MARGIN) + 'M_' + str(i) + '.pkl'
with open(title,'rb') as f:
    Original_dataset,ans_DBS = pkl.load(f)


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

#step 1#
x_1i = np.array(set_A[0])
x_2i = np.array(set_B[0])
x_1_list = []
x_2_list = []
p_1_list = []
p_2_list = []
#-- loop --#
epsilon = EPSILON
cond = 10
i = 0
while True:
	#step i#
	p_1i,g_1i = gl.PbarX_Max(x_1i,x_2i,set_A)
	p_2i,g_2i = gl.PbarX_Max(x_2i,x_1i,set_B)
	p_1_list.append(p_1i)
	p_2_list.append(p_2i)
	f_i = np.linalg.norm(x_1i-x_2i)
	mother1 = max(np.linalg.norm(x_1i - p_1i),np.sqrt(g_1i*f_i))
	mother2 = max(np.linalg.norm(x_2i - p_2i),np.sqrt(g_2i*f_i))
	if mother1 != 0:
		ratio1 = g_1i/mother1
	else:
		ratio1 = 0
	if mother2 != 0:
		ratio2 = g_2i/mother2
	else:
		ratio2 = 0

	cond = 1 - (f_i-(g_1i+g_2i))/f_i
	if ratio1 > ratio2:
		#update 1
		x_1i = gl.nextX2(p_1i,x_1i,x_2i)
	else:
		#update 2
		x_2i = gl.nextX2(p_2i,x_2i,x_1i)
	x_1_list.append(x_1i)
	x_2_list.append(x_2i)
	print('Dist: %.3f\tCondition: %.3f' % (f_i,cond))
	if cond <= epsilon:
	#if i > 5:
		break
	i += 1




#--test output--#
print('Dist: %.3f\tIteration:%d' % (f_i,i))
#print('x_1i',x_1i,'x_2i',x_2i)
pred_DBS = gl.weight(x_1i,x_2i)
print(pred_DBS)
print(ans_DBS/ans_DBS[0])
#--RMSE--#
RMSE = np.sqrt(sum([np.square(ans_DBS[p]/ans_DBS[0]-pred_DBS[p]) for p in range(len(pred_DBS))])/len(pred_DBS))

print('RMSE',RMSE)
OUTPUT_PATH = './result/pickle/'
# with open(OUTPUT_PATH+'x_imp.pkl','wb') as f:
# 	pkl.dump([x_1i,x_2i],f)
# with open(OUTPUT_PATH+'imp_list','wb') as f:
# 	pkl.dump([x_1_list,x_2_list,p_1_list,p_2_list],f)



#time_result.to_csv('./result/result_time&rate_100dim.csv',index=False)
#--Graph output--#
#plt.axes.Axes.set_title('Gilbert_Algorithm')
#plt.scatter(dataset['X'],dataset['Y'],label = 'dataset')
#plt.scatter(newX['X'],newX['Y'],label='Gilbert Algorithm_d_dim')
