import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#--animation--#
fig = plt.figure()
ims = []

#--import sample point set --#
dataset = pd.read_csv('dataset100_dist5.csv')

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
        #print('inner:',inner_px,set_P.loc[i,'X'],x['X'],set_P.loc[i,'Y'],x['Y'])
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
    xp_dist = np.sqrt(np.square(P['X']-x['X'])+np.square(P['Y']-x['Y']))
    unitXp = pd.Series([(P['X']-x['X'])/xp_dist,(P['Y']-x['Y'])/xp_dist],index=['X','Y'])
    xo = pd.Series([-x['X'],-x['Y']],index=['X','Y'])
    inner = unitXp['X']*xo['X']+unitXp['Y']*xo['Y']
    if inner < 0.0:
        thisX = x
        msg = 'ok'
    else:
        thisX = pd.Series([x['X']+unitXp['X']*inner,x['Y']+unitXp['Y']*inner],index=['X','Y'])
        #print('fuck',x,inner)
        msg='fuck'
    return thisX


result = pd.DataFrame()

#-- loop --#
epsilon = 0.01
cond = 10
newX = x1
print(x1)
#print('initial',newX)
newP = [p1,0]
i = 0
while True:
    newP = calcminPbarX(newX)
    #print(newP)
    #calc 1-epsilon approximation
    cond = 1.0 - (newP[1]/(np.sqrt(np.square(newX['X'])+np.square(newX['Y']))))

    #print('---------')
    #step start
    #print(calcNextX(newP[0],newX))
    newX = calcNextX(newP[0],newX)
    
    dist_newX = np.sqrt(np.square(newX['X'])+np.square(newX['Y']))
    #print('newX:',newP[0])
    
    print(i,'\tgap:',cond,'X:',dist_newX)

    #--animation--#
    #im = plt.scatter(dataset['X'],dataset['Y'],label = 'dataset')
    #im = plt.scatter(newX['abel = 'newX')
    im = plt.scatter(newP[0]['X'],newP[0]['Y'], label = 'newP')
    ims.append(im)

    outline = pd.DataFrame([[cond,dist_newX,newX['X'],newX['Y']]],columns=(['cond','dist_newX','X','Y']))

    result = result.append(outline,ignore_index=True)

    # less than epsilon
    if cond <= epsilon:
        break

    i += 1



#--Graph output--#
ani = animation.ArtistAnimation(fig,ims,interval=100)
ani.save("output.gif",writer="imagemagick")

#plt.show()