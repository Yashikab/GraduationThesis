import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
from datetime import datetime as dt

#--definition--#
num_list = [1000,5000,10000]
dim = 10
columnlist = []
for i in range(dim):
    columnlist.append('x' + str(i))

#--time result--#
time_result = pd.DataFrame()
start_time = dt.now().strftime('%s')

for num in num_list:
    #--import sample point set --#
    title = './datasets/dataset'+ str(num) +'_dist5_'+ str(dim) + 'dim.csv'

    dataset = pd.read_csv(title)

    #--set origin--#
    origin = dataset.loc[0,:]

    #--get set P --#
    set_num = len(dataset)
    set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)


    #step 1#
    #--calculate Minimum distance--#
    for i in range(1,set_num):
        '''x2_square = 0.
        for j in range(dim):
            x2_square += np.square(set_P.loc[i,columnlist[j]])'''

        dist = np.linalg.norm(set_P.loc[i,:])

        if i == 1:
            min_dist = dist
            x1 = set_P.loc[i,:]
        elif min_dist > dist:
            min_dist = dist
            x1 = set_P.loc[i,:]
    p1 = x1


    #step i#
    #--calculate min p|x--#
    def calcminPbarX(x):
        for i in range(1,set_num):
            '''inner_px = 0
            x_l2 = 0
            for j in range(dim):
                inner_px += set_P.loc[i,columnlist[j]]*x[columnlist[j]]
                x_l2 += np.square(x[columnlist[j]])
            PbarX = inner_px/np.sqrt(x_l2)'''

            inner_px = np.dot(set_P.loc[i,:],x)
            x_l2 = np.linalg.norm(x)
            PbarX = inner_px/x_l2


            if i == 1:
                minPbarX = PbarX
                minP = set_P.loc[i,:]
            elif minPbarX > PbarX:
                minPbarX = PbarX
                minP = set_P.loc[i,:]

        return [minP,minPbarX]

    #-- minimum distant on line segment(x,newp)--#
    def calcNextX(P,x):
        '''xp_l2 = 0

        for j in range(dim):
            xp_l2 += np.square(P[columnlist[j]]-x[columnlist[j]])'''
        P = np.array(P)
        x = np.array(x)
        xp_dist = np.linalg.norm(P - x)
        unitXP = (P - x)/xp_dist
        xo = (-1) * x
        '''for j in range(dim):
            unitXP_list.append((P[columnlist[j]]-x[columnlist[j]])/xp_dist)
            xo_list.append((-1)*x[columnlist[j]])
        unitXp = pd.Series(unitXP_list,index=columnlist)

        xo = pd.Series(xo_list,index=columnlist)'''

        '''inner = 0
        for j in range(dim):
            inner += unitXp[columnlist[j]]*xo[columnlist[j]]'''
        inner = np.dot(unitXP,xo)

        if inner < 0.0:
            thisX = x
            msg = 'ok'
        else:
            thisX_list = x + unitXP*inner
            '''for j in range(dim):
                thisX_list.append(x[columnlist[j]]+unitXp[columnlist[j]]*inner)'''
            thisX = pd.Series(thisX_list,index=columnlist)

        return thisX
    result = pd.DataFrame()


    #-- loop --#
    epsilon = 0.01
    cond = 10
    newX = x1

    #print('initial',newX)
    newP = [p1,0]
    i = 0
    total_time = 0
    while True:
        newP = calcminPbarX(newX)

        #calc 1-epsilon approximation
        '''dist_X = 0
        for j in range(dim):
            dist_X += np.square(newX[columnlist[j]])'''
        dist_X = np.linalg.norm(newX)
        cond = 1.0 - (newP[1]/dist_X)

        newX = calcNextX(newP[0],newX)
        '''dist_newX = 0
        for j in range(dim):
            dist_newX += np.square(newX[columnlist[j]])'''
        dist_newX = np.linalg.norm(newX)



        # less than epsilon
        if cond <= epsilon:
            break

        i += 1


    #--test output--#
    print('Dist: %.3f\tIteration:%d' % (dist_X,i))



  #result.to_csv('./result/result'+str(num)+'_'+str(dim)+'dim.csv',index=False)

#time_result.to_csv('./result/result_time&rate_100dim.csv',index=False)
#--Graph output--#
#plt.axes.Axes.set_title('Gilbert_Algorithm')
#plt.scatter(dataset['X'],dataset['Y'],label = 'dataset')
#plt.scatter(newX['X'],newX['Y'],label='Gilbert Algorithm_d_dim')
