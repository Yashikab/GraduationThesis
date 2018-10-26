import pickle as pkl
import numpy as np
import pandas as pd
#-- comment--#
'''
'This module is to calculate Minkowski difference
'Function needs dimension(int) & dataset(DataFrame)
'Function will return list as bellow form
'[Minkowski dataset, Base vector]
'Base vector is two points of each class
, which is necessary to calculate decision boundary surface in two classes space.
'''

def difference(dim,dataset):
	#--index --#
	columnlist = []
	for i in range(dim):
	    v_name = 'x' + str(i)
	    columnlist.append(v_name)
	#columnlist.append('label') # 1 or -1

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
	Original_A_data = pd.DataFrame([],columns=(columnlist))
	Original_B_data = pd.DataFrame([],columns=(columnlist))
	for a in range(len(set_A)):
		for b in range(len(set_B)):
			Minkowski = Minkowski.append(set_A.loc[a,columnlist] - set_B.loc[b,columnlist]
										,ignore_index=True)
			Original_A_data = Original_A_data.append(set_A.loc[a,columnlist],ignore_index=True)
			Original_B_data = Original_B_data.append(set_B.loc[a,columnlist],ignore_index=True)
			
	return [Minkowski,Original_A_data,Original_B_data]

def separate(dim,dataset):
	#--index --#
	columnlist = []
	for i in range(dim):
	    v_name = 'x' + str(i)
	    columnlist.append(v_name)
	columnlist.append('label') # 1 or -1

	set_A = pd.DataFrame([],columns=(columnlist))
	set_B = pd.DataFrame([],columns=(columnlist))

	#-- separate with class--#
	for i in range(len(dataset)):
		if dataset.loc[i,'label'] == 1:
			set_A = set_A.append(dataset.loc[i,columnlist],ignore_index=True)
		elif dataset.loc[i,'label'] == -1:
			set_B = set_B.append(dataset.loc[i,columnlist],ignore_index=True)
	return [set_A,set_B]
    
#set:dataframe, weight:ndarray,min:boolean(minimum:True)#
def search_sv(set,weight,min):
        
        for i in range(len(set)):
                sv_dot = np.dot(weight,np.array(set.loc[i,:]))
                if i == 0:
                        min_sv_dot = sv_dot
                        sv = np.array(set.loc[i,:])
                if min:
                        if sv_dot < min_sv_dot:
                                min_sv_dot = sv_dot
                                sv = np.array(set.loc[i,:])
                if not min:
                        if sv_dot > min_sv_dot:
                                min_sv_dot = sv_dot
                                sv = np.array(set.loc[i,:])
        return sv

if __name__ == '__main__':
	dim = 2
	num = 100
	#--load pickle--#
	title = '../datasets/pickle/2class_dataset'+ str(num) +'P_'+ str(dim) + 'dim.pkl'
	with open(title,'rb') as f:
	    dataset = pkl.load(f)

	Minkowski1,testA,testB = difference(dim,dataset)

	OUTPUT_PATH = '../datasets/pickle/'
	with open(OUTPUT_PATH+'Minkowski_'+ str(num) +'P_'+ str(dim) + 'dim.pkl','wb') as f:
		pkl.dump(Minkowski1,f)
