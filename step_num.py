import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pickle
import numpy as np


NUM_LIST = [300,500,700,1000,3000,5000]
#--load pickle--#
Step = []
for num in NUM_LIST:
    title = './result/pickle/result_Step_' + str(num) + 'P.pkl'
    with open(title,'rb') as f:
        Step.append(pickle.load(f))

#-- plot average --#
plt.plot(NUM_LIST,Step,label='Total Step')


#--set Params--#
plt.legend()
plt.title(u'Gilbert Algorithm Step')
plt.xlabel(u'#Points')
plt.ylabel(u'Time')
OUTPUT_PATH = './image/use in thesis/Ordinal_EACH_STEP.png'
plt.savefig(OUTPUT_PATH)