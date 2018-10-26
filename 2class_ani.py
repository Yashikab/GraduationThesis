#import matplotlib
#matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle as pkl

#--animation--#
fig = plt.figure()
ims = []

#--import sample point set --#
title = './datasets/pickle/2class_dataset50P_2dim.pkl'
with open(title,'rb') as f:
    dataset = pkl.load(f)
PATH = './result/pickle/'

with open(PATH+'imp_list','rb') as f:
    x_1_list,x_2_list,p_1_list,p_2_list = pkl.load(f)

#--animation Frame--#
def _update_plot(i):
    plt.clf()
    frame = plt.scatter(dataset['x0'],dataset['x1'],color='royalblue',marker='o')
    frame = plt.plot(p_1_list[i][0],p_1_list[i][1],color='deeppink',marker='x',markersize =10,label='p1')
    frame = plt.plot(p_2_list[i][0],p_2_list[i][1],color='deeppink',marker='x',markersize =10,label='p2')
    this_x = [x_1_list[i][0],x_2_list[i][0]]
    this_y = [x_1_list[i][1],x_2_list[i][1]]
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
                              frames = len(x_1_list),
                              interval = 500,
                              repeat = False)

ani.save('2class_animation.gif',writer='imagemagick')

#plt.axes().set_aspect('equal', 'datalim')
#plt.show()
