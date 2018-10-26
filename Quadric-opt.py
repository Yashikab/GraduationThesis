import pandas as pd
import numpy as np
import cvxopt as co
from cvxopt import matrix
import matplotlib.pyplot as plt
#--import sample point set --#
dataset = pd.read_csv('dataset100_dist5.csv')

#--set origin--#
origin = dataset.loc[0,:]

#--get set P --#
set_num = len(dataset)
set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)
train_matrix = []
restrict = []
for i in range(set_num):
    if i == 0:
        row = [origin['X'],origin['Y'],1.0]
    else:
        row = [(-1)*set_P.loc[i,'X'],(-1)*set_P.loc[i,'Y'],-1.0]
    train_matrix.append(row)
    restrict.append(-1.0)



#--set matrix--#
P = matrix(np.diag([2.0,2.0,0.0]))
q = matrix(np.array([0.0,0.0,0.0]))
G = matrix(np.array(train_matrix))
h = matrix(np.array(restrict))
#-- optimize --#
sol = co.solvers.qp(P,q,G,h)

#--calc distans (O,polytope)--#
w = pd.Series([sol['x'][0],sol['x'][1]],index=['X','Y'])
w_l2 = np.sqrt(np.square(w['X'])+np.square(w['Y']))
y_seg = pd.Series([0,(-1)*sol['x'][2]/sol['x'][1]],index=['X','Y'])
vec_yo = pd.Series([0,(-1)*y_seg['Y']],index=['X','Y'])
unit_dirc = pd.Series([w['Y']/w_l2,-w['X']/w_l2],index=['X','Y'])
inner = unit_dirc['X']*vec_yo['X']+unit_dirc['Y']*vec_yo['Y']

thisX = pd.Series([y_seg['X']+unit_dirc['X']*inner,y_seg['Y']+unit_dirc['Y']*inner],index = ['X','Y'])

#--Graph output--#
plt.scatter(dataset['X'],dataset['Y'],label='dataset')
x = np.arange(0,5,0.01)
y = (-1)*(sol['x'][0]*x/sol['x'][1] + 2*sol['x'][2]/sol['x'][1])
plt.plot(x,y,label='Q-opt')
plt.scatter(2*thisX['X'],2*thisX['Y'],label='QP')
#plt.show()
