# -*- coding: utf-8 -*-
import sys
sys.path.append('./module')
import numpy as np
import pandas as pd
import pickle as pkl
import Gilbert as gl
# ユークリッド距離
def distance(a, b):
    return np.linalg.norm(a-b)

# 線分abと線分acについて内積
def naiseki(a, b, c):
    return np.dot(b-a, c-a)

# 線分abと線分acについて外積 / 使ってない
def gaiseki(a, b, c):
    return np.cross(b-a, c-a)

# クラスaについて，点cを始点としてbを現在の解としたときにギルバートを1ステップ
def mutual_update(set_P, x_1, x_2, epsilon):
    dist = np.linalg.norm(x_1 - x_2)

    # 現在の距離よりも近い点があったらそれを現在の解pとして更新
    dist_list = [np.linalg.norm(p - x_2) for p in set_P]
    argmin_kyoritachi = np.argmin(dist_list)
    update_point = False
    if dist > np.min(dist_list):
        x_1 = set_P[np.argmin(dist_list)]
        dist = np.min(dist_list)
        update_point = True
    # 現在の解よりも距離が短いp|xがあったら最短距離を計算して次の解とする
    minP, minPbarX = gl.PbarX_Min(x_2,x_1,set_P)
    #print(minP,minPbarX)
    if dist > minPbarX:
        if np.linalg.norm(x_1 - minP) == 0:
            if update_point == False:
                return None
            else:
                return x_1

        # naiseki_waru_nagasa = naiseki(c, b, a[argmin_shaeikyori]) / kyori
        # cb_mainasu_nagasa = kyori - naiseki_waru_nagasa
        # kyori_ab = distance(b, a[argmin_shaeikyori])
        # maruhi = kyori * cb_mainasu_nagasa / kyori_ab
        # wariai = maruhi / kyori_ab

        next_x = gl.nextX2(minP,x_1,x_2)
        #print(next_x)
        if update_point == False and 1 - minPbarX/dist < epsilon:
            #print(dist)
            return None
        return next_x

    # 解の更新が無かったらNone
    if update_point == False:
        return None
    else:
        return x_1

# クラスaとクラスbの多面体距離を求める
def main(set_A, set_B, epsilon):
    x1 = set_A[0]
    dist_list = [np.linalg.norm(x1 - x) for x in set_B]
    x2 = set_B[np.argmin(dist_list)]

    #"""
    # 毎回変更する版
    A_flag = True
    B_flag = True
    itr = 0
    # どちらの点も更新が行われなかったら終了
    while(A_flag == True or B_flag == True):
        A_flag = True
        B_flag = True

        update = mutual_update(set_A, x1, x2, epsilon)
        #if asada == None:
        if not isinstance(update, np.ndarray):
            A_flag = False
        else:
            x1 = update

        update = mutual_update(set_B, x2, x1, epsilon)
        #if asada == None:
        if not isinstance(update, np.ndarray):
            B_flag = False
        else:
            x2 = update
        itr += 1
        print(np.linalg.norm(x1 - x2)) 

    """
    # 収束してから変更する版
    # できてない
    sokuochi_a = False
    sokuochi_b = False
    while(sokuochi_a == False or sokuochi_b == False):
        sokuochi_a = True
        sokuochi_b = True
        asada = np.array([[0, 0, 0]])
        while(isinstance(asada, np.ndarray)):
        #while(asada != None):
            asada = aidu(a, a_kai, b_kai, epsilon)
            print("adsfa", asada)
            #if asada != None:
            if not isinstance(asada, np.ndarray):
                a_kai = asada
                sokuochi_a = False

        asada = np.array([[0, 0, 0]])
        while(isinstance(asada, np.ndarray)):
        #while(asada != None):
            asada = aidu(b, b_kai, a_kai, epsilon)
            print("wert", asada)
            #if asada != None:
            if not isinstance(asada, np.ndarray):
                b_kai = asada
                sokuochi_b = False

        print(a_kai, b_kai, distance(a_kai, b_kai))
    """

    # 計算が終わったら値を返す
    return (x1, x2,itr)

# mine関数 踏むと爆発
if __name__ == "__main__":
    #a = np.array([[0., 0.], [2., 0.], [1., 1.]])
    #b = np.array([[0., 2.], [2., 2.], [1., 3.], [0.5, 2.01], [1.5, 2.01]])
    #a = np.array([[0., 0., 0.], [2., 0., 0.], [0., 2., 0.], [2., 2., 0.]])
    #b = np.array([[0., 0., 5.], [3., 0., 4.], [0., 3., 4.], [3., 3., 5.]])
    #b = np.array([[0., 0., 3.]])
    #a = np.array([[0., 0.], [0.5, 1.]])
    #b = np.array([[1., 0.], [1., 3.]])
    #a = np.array([[2., 0., 0.], [0., 1., 0.], [0., 0., 1.]])
    #b = np.array([[-1., 0., 0.], [0., -1., 0.], [0., 0., -1.]])
    #--index --#
    num = 10000
    DIM = 10
    with open('./datasets/pickle/2class_dataset' + str(num) + 'P_'+str(DIM)+'dim.pkl','rb') as f:
        dataset = pkl.load(f)
    dataset = np.array(dataset)
    set_A = []
    set_B = []

    #-- separate with class--#
    for data in dataset:
        if data[DIM] == 1:
            set_A.append([data[d] for d in range(DIM)])
        elif data[DIM] == -1:
            set_B.append([data[d] for d in range(DIM)])
    a = np.array(set_A)
    b = np.array(set_B)

    # 丸め誤差頻発マン
    #np.seterr(all='ignore')
    epsilon = 0.5

    # aとbを別のクラスとしてsvm計算   各端点をa_kai, b_kaiとする
    a_kai, b_kai, itr = main(a, b, epsilon)
    points = [a_kai,b_kai]
    print(gl.weight(a_kai,b_kai))
    with open('./result/pickle/kikuchi_weight.pkl','wb') as f:
        pkl.dump(gl.weight(a_kai,b_kai),f)
    print('distance:',distance(a_kai, b_kai),'Iteration:',itr)
