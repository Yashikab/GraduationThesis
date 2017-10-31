import pandas as pd
import numpy as np


#--import sample point set --#
dataset = pd.read_csv('dataset_dist5.csv')

#--set origin--#
origin = dataset.loc[0,:]

#--get set P --#
set_num = len(dataset)
set_P = pd.DataFrame(dataset.tail(set_num-1),copy=True)


#step 1#
#--calculate Minimum distance--#
for i in range(1,set_num):
    dist = np.sqrt(np.square(set_P.loc[i,'X'])+np.square(set_P.loc[i,'Y']))
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
        inner_px = set_P.loc[i,'X']*x['X'] + set_P.loc[i,'Y']*x['Y']
        PbarX = inner_px/np.sqrt(np.square(x['X'])+np.square(x['Y']))
        if i == 1:
            minPbarX = PbarX
            minP = set_P.loc[i,:]
        elif minPbarX > PbarX:
            minPbarX = PbarX
            minP = set_P.loc[i,:]


    return [minP,minPbarX]


#-- minimum distant on line segment(x,newp)--#
def calcNextX(P,x):
    xp_dist = np.sqrt(np.square(P['X']-x['X'])+np.square(P['Y']-x['X']))
    unitXp = pd.Series([(P['X']-x['X'])/xp_dist,(P['Y']-x['Y'])/xp_dist],index=['X','Y'])
    xo = pd.Series([-x['X'],-x['Y']],index=['X','Y'])
    inner = unitXp['X']*xo['X']+unitXp['Y']*xo['Y']
    if inner < 0:
        thisX = x
    else:
        thisX = pd.Series([x['X']+unitXp['X']*inner,x['Y']+unitXp['Y']*inner],index=['X','Y'])

    return thisX

#-- loop --#
epsilon = 0.01
cond = 10
newX = x1
newP = [p1,0]
while True:
    newP = calcminPbarX(newX)
    newX = calcNextX(newP[0],newX)
    dist_newX = np.sqrt(np.square(newX['X'])+np.square(newX['Y']))
    #calc 1-epsilon approximation
    cond = 1.0 - (newP[1]/(np.sqrt(np.square(newX['X'])+np.square(newX['Y']))))
    print(dist_newX)
    # less than epsilon
    if cond <= epsilon:
        break

    
