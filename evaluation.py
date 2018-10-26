import sys
sys.path.append('./module')
import pandas as pd
import numpy as np
import twoclassalg as alg
import pickle as pkl
from tqdm import tqdm
from datetime import datetime as dt
#--read file--#
DATA_NUM = 5
DATA_PATH = './datasets/pickle/2class_d/'
DIM = 10
NUM = 10000
MARGIN_LIST = [0.1,0.2,0.3]
DATASET_LIST = [[] for i in range(DATA_NUM)]

for i in range(DATA_NUM):
    for m in MARGIN_LIST:
        title = DATA_PATH + '2class_dataset' + str(NUM) + 'P_' + str(DIM) + 'dim_' + str(m) + 'M_' + str(i) + '.pkl'
        #dataset = pd.read_csv(title)
        with open(title,'rb') as f:
            dataset,ans = pkl.load(f)
        DATASET_LIST[i].append(np.array(dataset))


#--create lists--#
QP_DBS = [[] for i in range(DATA_NUM)]
QP_ck = [[] for i in range(DATA_NUM)]
CORE_DBS = [[] for i in range(DATA_NUM)]
CORE_itr = [[] for i in range(DATA_NUM)]
CORE_time = [[] for i in range(DATA_NUM)]
CORE_ck = [[] for i in range(DATA_NUM)]
KIKU_DBS = [[] for i in range(DATA_NUM)]
KIKU_itr = [[] for i in range(DATA_NUM)]
KIKU_time = [[] for i in range(DATA_NUM)]
KIKU_ck = [[] for i in range(DATA_NUM)]
DIKU_DBS = [[] for i in range(DATA_NUM)]
DIKU_itr = [[] for i in range(DATA_NUM)]
DIKU_time = [[] for i in range(DATA_NUM)]
DIKU_ck = [[] for i in range(DATA_NUM)]
#--run Algorithms--#
EPSILON = 0.01
for i in range(DATA_NUM):
    for m, ml in enumerate(MARGIN_LIST):
        print(f'Data:{i} Margin:{ml}')
        #--separate class--#
        set_A = []
        set_B = []
        for data in DATASET_LIST[i][m]:
            if data[DIM] == 1:
                set_A.append([data[d] for d in range(DIM)])
            elif data[DIM] == -1:
                set_B.append([data[d] for d in range(DIM)])
        set_A = np.array(set_A)
        set_B = np.array(set_B)

        # q_DBS = alg.quadratic(DATASET_LIST[i][m],DIM)
        c_DBS,c_itr,c_time = alg.coresets(EPSILON,set_A,set_B)
        k_DBS,k_itr,k_time = alg.kikuchi(EPSILON,set_A,set_B)
        d_DBS,d_itr,d_time = alg.dist_kikuchi(EPSILON,DATASET_LIST[i][m],DIM)
        #QP_ck[i].append(alg.ckcorrect(set_A,set_B,q_DBS))
        CORE_ck[i].append(alg.ckcorrect(set_A,set_B,c_DBS))      
        KIKU_ck[i].append(alg.ckcorrect(set_A,set_B,k_DBS))
        DIKU_ck[i].append(alg.ckcorrect(set_A,set_B,d_DBS))   
        #QP_DBS[i].append(q_DBS/np.max(np.abs(q_DBS)))
        CORE_DBS[i].append(c_DBS/np.max(np.abs(c_DBS)))
        CORE_itr[i].append(c_itr)
        CORE_time[i].append(c_time)
        KIKU_DBS[i].append(k_DBS/np.max(np.abs(k_DBS)))
        KIKU_itr[i].append(k_itr)
        KIKU_time[i].append(k_time)
        DIKU_DBS[i].append(d_DBS/np.max(np.abs(d_DBS)))
        DIKU_itr[i].append(d_itr)
        DIKU_time[i].append(d_time)


# with open('./result/pickle/evaluation.pkl','wb') as f:
#     pkl.dump((QP_DBS,CORE_DBS,CORE_itr,KIKU_DBS,KIKU_itr),f)

#--create pandas--#
columnlist = ['Type','Margin','CORE_ck','KIKU_ck','DIKU_ck','C_itr','K_itr','D_itr','C_time','K_time','D_time']
result = pd.DataFrame([],columns=(columnlist))
for i in range(DATA_NUM):
    for m in range(len(MARGIN_LIST)):
        # C_RMSE = alg.RMSE(QP_DBS[i][m],CORE_DBS[i][m])
        # K_RMSE = alg.RMSE(QP_DBS[i][m],KIKU_DBS[i][m])
        # D_RMSE = alg.RMSE(QP_DBS[i][m],DIKU_DBS[i][m])
        line = [i, MARGIN_LIST[m], CORE_ck[i][m], KIKU_ck[i][m], DIKU_ck[i][m], CORE_itr[i][m], KIKU_itr[i][m],DIKU_itr[i][m],
                CORE_time[i][m], KIKU_time[i][m], DIKU_time[i][m]]
        newvar = pd.DataFrame([line],columns=(columnlist))
        result = result.append(newvar,ignore_index=True)
# print(result)
# #print(ans_ck)
result.to_csv('./result/evaluation_faster.csv',index=False)
# with open('./result/pickle/evaluation.pkl','wb') as f:
#     pkl.dump(result,f)


