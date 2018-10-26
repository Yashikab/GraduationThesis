import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle
import numpy as np


NUM_LIST = [300,500,1000,5000,10000]
#--load pickle--#
P = []
for num in NUM_LIST:
    title = './result/pickle/Ordinal/result_Ordinal_' + str(num) + 'P.pkl'
    with open(title,'rb') as f:
        P.append(pickle.load(f))

#-- average , error --#
ERR = []
avg_P = []
for i in range(len(NUM_LIST)):
    avg_P.append(np.average(P[i]))
    ERR.append(np.std(P[i]))
    
    
avg_P = np.array(avg_P)
    
#-- plot average --#
plt.plot(NUM_LIST,avg_P,color = 'b',label='Time[sec] in Each Step')

#-- errorbar --#
plt.errorbar(NUM_LIST,avg_P,yerr=ERR,fmt='ro',ecolor='g')


#--set Params--#
plt.legend()
plt.title(u'Average time in one step')
plt.xlabel(u'#Points')
plt.ylabel(u'sec')
#--save png--#
OUTPUT_PATH = './image/use in thesis/Ordinal_EACH_STEP.png'
plt.savefig(OUTPUT_PATH)