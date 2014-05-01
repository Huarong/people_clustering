# scoding=utf-8

import matplotlib.pyplot as plt
import copy
import numpy as np
from collections import defaultdict,Counter
from RandSample import rand_2D_vector_rect,rand_2D_vector_circle,real_matrix,noise_2D_vector_rect
from util import euclidean_distance,cosine_distance,min_Angle_part,draw_line
from AD_Cluster import AD_Cluster



def cutNoise(matrix):
    print "total:",len(matrix)
    '''
    适用类似基于密度聚类的方法，识别样本中的无意义样本（特征过少），和
    噪声样本（不属于任何类，或自成一类）
    '''

    discard = []        # discard 无需返回， 根据 noise 和 real 可以得出
    noise = []
    real = []
    noise_matrix = []
    real_matrix = []

    rest = []
    rm = False
    if(len(matrix[0])>100):
        rm = True
    for i,vector in enumerate(matrix):
        No_0 = 0                        # 记录非零特征
        for j in vector:
            if 0!=j:
                No_0 += 1
        if rm:
            low = 3
        else:
            low = 1

        if (low > No_0):                # discard 掉特征数量小于下限的向量
            discard.append(i)
        else:
            real.append(i)
            rest.append(vector)

    print "discard:",len(discard)
    #---------------------------------------------------------------------------------------          
    l = len(rest)
    distList = np.zeros((l,l),np.float)
    for i in range(l):
        distList[i][i] = float('inf')       # 自身不参与聚类比较
        for j in range(i+1,l):
            distList[i][j] = euclidean_distance(np.array(rest[i]), np.array(rest[j]))
            distList[j][i] = distList[i][j]
            if(distList[i][j]==0):
                print i,":",rest[i]
                print j,":",rest[j]
    #----------------------------------------------------------------------------------------
    mostSimList = []        # 记录与第 i 个样本第 m 相似的距离
    m = 1
    if(l<=m):
        noise = copy.copy(real)
        real = []
        noise_matrix = rest
        real_matrix = []
        tmp = []
        angles = []
        return real_matrix,noise_matrix,tmp,angles,real,noise

    marks = [i for i in range(l)]

    for i in range(l):
        lis = distList[i].tolist()
        lis = sorted(lis)
        mostSimList.append(lis[m-1])

    ADist = zip(marks,mostSimList)
    ADist = sorted(ADist, key = lambda x: x[1], reverse=True)


    end = l-1
    Dlist = []
    while  end>=0:
        Dlist.append(ADist[end][1])
        end -= 1
    print Dlist
    draw_line(Dlist)

    tmp, angles, part = min_Angle_part(Dlist)    # 注意 Dlist 里面应该是从小到大的顺序
    print part

    for e in ADist[0:(1+part)*l/10]:
        noise.append(real[e[0]])

    real0 = copy.copy(real)                 # 对应 rest 中的向量

    real = sorted(list(set(real) - set(noise)))
    noise = sorted(noise) 

    real_matrix = []
    for i , vector in enumerate(rest):
        if real0[i] in noise:
            noise_matrix.append(vector)
        else:
            real_matrix.append(vector)
    return real_matrix,noise_matrix,tmp,angles,real,noise


def demo():
    from util import load_matrix,draw_line,draw_2D_noise
    points = load_matrix("./pickle/matrix/Alice_Gilbreath.matrix")
    # points = noise_2D_vector_rect(200, 3)
    # points.append((0,0))
    # points.append((0,0))
    vectors = [list(e) for e in points]

    realPTs, noisePTs,tmp,angles,real,noise = cutNoise(vectors)
    print "realPTs",len(realPTs),"real",len(real)
    print "noisePTs,",len(noisePTs),"noise",len(noise)
    print tmp
    print angles
    draw_line(tmp)
    draw_line(angles)
    draw_2D_noise(realPTs, noisePTs)

    cluster1 = AD_Cluster()
    # vectors0 = [np.array(f) for f in points]
    vectors1 = [np.array(f) for f in realPTs]
    # cluster1.cluster(vectors0)
    # cluster1.cluster(vectors1)

if __name__=="__main__":
    demo()
