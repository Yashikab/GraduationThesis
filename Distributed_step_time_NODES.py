import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle
import numpy as np


#NUM_LIST = [500,1000,3000,5000,10000]
NUM = 10000
NODES_LIST = [1,5,10,30,50]
PATH = './result/pickle/'
#--load pickle--#
Dist_P = []

NODES_P = []
for NODE in NODES_LIST:
	dist_title = PATH + 'Distributed/result_Distributed_' + str(NUM) + 'P_' + str(NODE) + 'NODES.pkl'
	with open(dist_title,'rb') as f:
		Dist_P.append(pickle.load(f))

	


#-- average , error --#
ERR_Dist = []
avg_Dist_P = []

for i in range(len(NODES_LIST)):
	avg_Dist_P.append(np.average(Dist_P[i]))
	ERR_Dist.append(np.std(Dist_P[i]))

for j in range(len(NODES_LIST)):    
	avg_Dist_P = np.array(avg_Dist_P)

    
#-- plot average --#
bar_list = [':','-.','--','-']
marker_list = ['o','x','D','s','v']
color_list = ['black','gray']
print(avg_Dist_P)
plt.plot(np.array(NODES_LIST),1/np.array(avg_Dist_P),color='royalblue'
							,marker='o'
							,linestyle='-'
							,label='Distributed')


#-- errorbar --#
#plt.errorbar(NODES_LIST,avg_Dist_P,color= 'black',yerr=ERR_Dist,ecolor='gray')

#--set Params--#
plt.legend()
plt.title(u'Time in Each Node')
plt.xlabel(u'#Nodes')
plt.ylabel(u'1/sec')

OUTPUT_PATH = './image/use in thesis/Distributed_NODES_time3.png'
plt.savefig(OUTPUT_PATH)
