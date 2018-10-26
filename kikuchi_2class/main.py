# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import pickle as pkl

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
def aidu(a, b, c, epsilon):
    kyori = distance(b, c)

    # 現在の距離よりも近い点があったらそれを現在の解pとして更新
    kyoritachi = [distance(i, c) for i in a]
    argmin_kyoritachi = np.argmin(kyoritachi)
    point_koushin = False
    if kyori > kyoritachi[argmin_kyoritachi]:
        b = a[argmin_kyoritachi]
        kyori = kyoritachi[argmin_kyoritachi]
        point_koushin = True
    # 現在の解よりも距離が短いp|xがあったら最短距離を計算して次の解とする
    shaeikyori = [naiseki(c, b, i) / kyori for i in a]
    argmin_shaeikyori = np.argmin(shaeikyori)
    print(a[argmin_shaeikyori],shaeikyori[argmin_shaeikyori])
    if kyori > shaeikyori[argmin_shaeikyori]:
        if distance(b, a[argmin_shaeikyori]) == 0:
            if point_koushin == False:
                return None
            else:
                return b

        naiseki_waru_nagasa = naiseki(c, b, a[argmin_shaeikyori]) / kyori
        cb_mainasu_nagasa = kyori - naiseki_waru_nagasa
        kyori_ab = distance(b, a[argmin_shaeikyori])
        maruhi = kyori * cb_mainasu_nagasa / kyori_ab
        wariai = maruhi / kyori_ab

        next_x = a[argmin_shaeikyori] * wariai + b * (1 - wariai)
        #print(next_x)
        if point_koushin == False and kyori - distance(c, next_x) < epsilon * kyori:
            #print(kyori, distance(c, next_x), kyori - distance(c, next_x), epsilon * kyori)
            return None
        return next_x

    # 解の更新が無かったらNone
    if point_koushin == False:
        return None
    else:
        return b

# クラスaとクラスbの多面体距離を求める
def main(a, b, epsilon):
    a_kai = a[0]
    kyoritachi = [distance(a_kai, i) for i in b]
    argmin_ab = np.argmin(kyoritachi)
    b_kai = b[argmin_ab]

    #"""
    # 毎回変更する版
    a_flag = True
    b_flag = True
    # どちらの点も更新が行われなかったら終了
    while(a_flag == True or b_flag == True):
        a_flag = True
        b_flag = True

        asada = aidu(a, a_kai, b_kai, epsilon)
        #if asada == None:
        if not isinstance(asada, np.ndarray):
            a_flag = False
        else:
            a_kai = asada

        asada = aidu(b, b_kai, a_kai, epsilon)
        #if asada == None:
        if not isinstance(asada, np.ndarray):
            b_flag = False
        else:
            b_kai = asada

        print(a_kai, b_kai, distance(a_kai, b_kai))

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
    return (a_kai, b_kai)

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
    columnlist = ['x0','x1']
    
    with open('../datasets/pickle/2class_dataset50P_2dim.pkl','rb') as f:
        dataset = pkl.load(f)

    set_A = pd.DataFrame([],columns=(columnlist))
    set_B = pd.DataFrame([],columns=(columnlist))

    #-- separate with class--#
    for i in range(len(dataset)):
        if dataset.loc[i,'label'] == 1:
            set_A = set_A.append(dataset.loc[i,columnlist],ignore_index=True)
        elif dataset.loc[i,'label'] == -1:
            set_B = set_B.append(dataset.loc[i,columnlist],ignore_index=True)

    a = np.array(set_A)
    b = np.array(set_B)

    # 丸め誤差頻発マン
    #np.seterr(all='ignore')
    epsilon = 0.01

    # aとbを別のクラスとしてsvm計算   各端点をa_kai, b_kaiとする
    a_kai, b_kai = main(a, b, epsilon)
    points = [a_kai,b_kai]
    #with open('../result/pickle/kikuchi.pkl','wb') as f:
    #    pkl.dump(points,f)
    print("\nresult: a: " + str(a_kai) + ", b: " + str(b_kai) + ", distance: " + str(distance(a_kai, b_kai)))
