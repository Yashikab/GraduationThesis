#import matplotlib
#matplotlib.use('Agg')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
import math
#--animation--#
fig = plt.figure()
ims = []

#--import sample point set --#
dataset = pd.read_csv('./datasets/dataset500_dist5.csv')
PKL_PATH = './result/pickle/Dist_ani/'
NODES = 3

#-- open pickle file --#
with open(PKL_PATH + 'choose_P.pkl','rb') as f:
    choose_P = pickle.load(f)

with open(PKL_PATH + 'choose_x.pkl','rb') as f:
    choose_x = pickle.load(f)

with open(PKL_PATH + 'P_from_node.pkl','rb') as f:
    P_from_node = pickle.load(f)


#--devide origin&data--#
origin = dataset.loc[0,:]
data = pd.DataFrame(dataset[1:])
SET_NUM = len(data)
data = data.reset_index(drop=True)

#--get set P (separate for nodes)--#
EACH_SET = math.ceil(len(dataset) / NODES)
set_P = []
for i in range(0,SET_NUM,EACH_SET):
    if i+EACH_SET >= SET_NUM:
        node_data = pd.DataFrame(data[i:])
    else:
        node_data = pd.DataFrame(data[i:i+EACH_SET])
    node_data = node_data.reset_index(drop=True)
    set_P.append(node_data)


#--animation Frame--#
def _update_plot(i):
    plt.clf()
    plt.scatter(origin['X'],origin['Y'],color='black',marker='o')
    plt.scatter(set_P[0]['X'],set_P[0]['Y'],color='royalblue',marker='o')
    plt.scatter(set_P[1]['X'],set_P[1]['Y'],color='darkorange',marker='o')
    plt.scatter(set_P[2]['X'],set_P[2]['Y'],color='darkmagenta',marker='o')
    this_x = [0,choose_x[i][0]]
    this_y = [0,choose_x[i][1]]
    plt.plot(this_x,this_y,color='orangered',marker='.',markersize = 5)
    plt.plot(P_from_node[0][i][0]['X'],P_from_node[0][i][0]['Y'],color='lime',marker='*',markersize=10)
    plt.plot(P_from_node[1][i][0]['X'],P_from_node[1][i][0]['Y'],color='lime',marker='*',markersize=10)
    plt.plot(P_from_node[2][i][0]['X'],P_from_node[2][i][0]['Y'],color='lime',marker='*',markersize=10)
    plt.plot(choose_P[i][0]['X'],choose_P[i][0]['Y'],color='deeppink',marker='x',markersize =10)
    plt.axes().set_aspect('equal', 'datalim')
    #if len(im) > 0:
    #    im[0].remove()
    #    im.pop()
    #im.append(frame)
    title = "./image/Dist_frame/frame" + str(i) + ".png"
    plt.savefig(title)

#--Graph output--#
fig = plt.figure()
                       
ani = animation.FuncAnimation(fig,_update_plot,
                              frames = len(choose_P),
                              interval = 500,
                              repeat = False)

ani.save('Dist_animation.gif',writer='imagemagick')

#plt.axes().set_aspect('equal', 'datalim')
#plt.show(