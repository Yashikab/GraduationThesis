import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle
import numpy as np


EPSILON_LIST = [0.1,0.05,0.01,0.005,0.001]
#--load pickle--#
Step = []
for epsilon in EPSILON_LIST:
    title = './result/pickle/result_EpsilonStep_' + str(epsilon) + '.pkl'
    with open(title,'rb') as f:
        Step.append(pickle.load(f))
#print(1/np.array(Step))
#-- plot average --#
plt.plot(1/np.array(EPSILON_LIST),np.array(Step),color='royalblue',marker = 'o',label='Step time')


#--set Params--#
plt.legend()
plt.title(u'Step time in each $\epsilon$ value')
plt.xlabel(u'$1/\epsilon$')
plt.ylabel(u'Step')

#--save png--#
OUTPUT_PATH = './image/Step_Epsilon_Gilbert2.png'
plt.savefig(OUTPUT_PATH)
