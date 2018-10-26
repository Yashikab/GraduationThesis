# 2D CONVEXHULL
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from random import random, gauss



def conv(p):
    p = np.sort(p)

    # p1 -> p2 -> p3: clockwise rotation
    clockwise = lambda p1,p2,p3: (p2[1]-p1[1])/(p2[0]-p1[0])>(p3[1]-p2[1])/(p3[0]-p2[0])
        
    # Upper hull
    Lu = [p[0],p[1]]
    for i in range(2,N):
        Lu.append(p[i])
        while (len(Lu) >= 3) and not clockwise(Lu[-3], Lu[-2], Lu[-1]):
            Lu.remove(Lu[-2])
        else:
            pass

    # Lower hull
    Ll = [p[-1], p[-2]]
    for i in range(N-3, -1, -1):
        Ll.append(p[i])
        while (len(Ll) >= 3) and not clockwise(Ll[-3], Ll[-2], Ll[-1]):
            Ll.remove(Ll[-2])
        else:
            pass

    # Convex hull
    Lc = Lu + Ll
    Lc = sorted(set(Lc), key=Lc.index)
    return Lc

if __name__ == '__main__':
    # Make points
    N = 1500
    p = [[gauss(0.3, 0.01), gauss(0.5, 0.1)] for i in range(N)]

    Lc = conv(np.array(p))

    # Ploting result
    pp = np.array(p).T
    plt.plot(pp[0], pp[1], "ko")

    Nc = len(Lc)
    p1 = Lc[0]
    for i in range(Nc-1):
        p2 = Lc[i+1]
        plt.plot((p1[0], p2[0]), (p1[1], p2[1]), "b-")
        p1 = p2
    p1, p2 = Lc[0], Lc[-1]
    plt.plot((p1[0], p2[0]), (p1[1], p2[1]), "b-")

    plt.savefig('fuck.png')