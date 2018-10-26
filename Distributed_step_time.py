import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle
import numpy as np


NUM_LIST = [500,1000,3000,5000,10000]
NODES_LIST = [1,5,10,30,50]
PATH = './result/pickle/'
#--load pickle--#
Ord_P = []
Dist_P = []
for num in NUM_LIST:
	ord_title = PATH + 'Ordinal/result_Ordinal_' + str(num) + 'P.pkl'
	NODES_P = []
	for NODE in NODES_LIST:
		dist_title = PATH + 'Distributed/result_Distributed_' + str(num) + 'P_' + str(NODE) + 'NODES.pkl'

		with open(dist_title,'rb') as f:
			NODES_P.append(pickle.load(f))
	Dist_P.append(NODES_P)
	with open(ord_title,'rb') as f:
		Ord_P.append(pickle.load(f))



#-- average , error --#
ERR_Dist = []
ERR_Ord = []
avg_Dist_P = []
avg_Ord_P = []
for i in range(len(NUM_LIST)):
    avg_Ord_P.append(np.average(Ord_P[i]))
    ERR_Ord.append(np.std(Ord_P[i]))



for j in range(len(NODES_LIST)):
	EACH_avg = []
	EACH_ERR = []
	for i in range(len(NUM_LIST)):
		EACH_avg.append(np.average(Dist_P[i][j]))
		EACH_ERR.append(np.std(Dist_P[i][j]))
	avg_Dist_P.append(EACH_avg)
	ERR_Dist.append(EACH_ERR)

avg_Ord_P = np.array(avg_Ord_P)

for j in range(len(NODES_LIST)):    
	avg_Dist_P[j] = np.array(avg_Dist_P[j])

    
#-- plot average --#
bar_list = [':','-.','--','-']
marker_list = ['o','x','D','s','v']
color_list = ['red','orangered','cyan','green','fuchsia']
for j in range(len(NODES_LIST)):
	plt.plot(NUM_LIST,avg_Dist_P[j],color = color_list[j%5]
									,marker = marker_list[j%5]
									,linestyle=bar_list[3]
									,label='Distributed_'+ str(NODES_LIST[j]) + 'NODES')

plt.plot(NUM_LIST,avg_Ord_P,color='gray'
							,marker='o'
							,linestyle='--'
							,label='Non_Distributed')


#-- errorbar --#
#for j in range(len(NODES_LIST)):
#	plt.errorbar(NUM_LIST,avg_Dist_P[j],yerr=ERR_Dist[j],fmt=color_list[j%5] + marker_list[j%5],ecolor='g')
#plt.errorbar(NUM_LIST,avg_Ord_P,color= 'black',yerr=ERR_Ord,ecolor='gray')

#--set Params--#
plt.legend()
plt.title(u'Step Time')
plt.xlabel(u'#Points')
plt.ylabel(u'sec')

OUTPUT_PATH = './image/time/Ordinal_time.png'
plt.savefig(OUTPUT_PATH)
