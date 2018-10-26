#import matplotlib
#matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle

#--animation--#
fig = plt.figure()
ims = []

#--import sample point set --#
dataset = pd.read_csv('./datasets/dataset500_dist5.csv')

PATH = './result/pickle/Ordinal_ani/'
#-- open pickle file --#
with open(PATH+'allP.pkl','rb') as f:
    allP = pickle.load(f)

with open(PATH+'allX.pkl','rb') as f:
    allX = pickle.load(f)

#--animation Frame--#
def _update_plot(i):
    plt.clf()
    frame = plt.scatter(dataset['X'],dataset['Y'],color='royalblue',marker='o')
    frame = plt.plot(allP[i][0][0],allP[i][0][1],color='deeppink',marker='x',markersize =10,label='p')
    this_x = [0,allX[i][0]]
    this_y = [0,allX[i][1]]
    frame = plt.plot(this_x,this_y,color='orangered',marker='.',markersize = 5,label='x')
    frame = plt.axes().set_aspect('equal', 'datalim')
    #if len(im) > 0:
    #    im[0].remove()
    #    im.pop()
    #im.append(frame)
    title = "./image/frame/frame" + str(i) + ".png"
    plt.savefig(title)

#--Graph output--#
fig = plt.figure()
                       
ani = animation.FuncAnimation(fig,_update_plot,
                              frames = len(allP),
                              interval = 500,
                              repeat = False)

ani.save('animation.gif',writer='imagemagick')

#plt.axes().set_aspect('equal', 'datalim')
#plt.show()
