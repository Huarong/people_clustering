#coding: utf-8

import numpy
import os
from util import load_matrix

'''   半随机生成 n 个二维点样本， 属于 m 个类, 类以方格交替分布 '''
def rand_2D_vector_rect(n,m):

    import random
    ms = numpy.sqrt(2*m)
    if(ms>int(ms)):     # 向上取整
        ms = int(ms) + 1
    else:
        ms = int(ms)

    tmp = []
    count = 0
    c = int(n/m)
    if(c < float(n)/m): # 向上取整（没格的元素个数）
        c += 1

    w = n/(2*ms)
    # cNum = 0
    for i in range(ms):
        for j in range(ms):
            if((i%2)==(j%2)):
                pi0 = i*w
                pj0 = j*w
                pi1 = (i+1)*w
                pj1 = (j+1)*w
                ccount = 0
                while ccount<c:
                    x = random.randint(pi0, pi1)
                    y = random.randint(pj0, pj1)
                    tu = (x,y)
                    if(tu not in tmp):
                        tmp.append(tu)
                        count += 1
                        ccount += 1
                        if(n==count):
                            return tmp
                # cNum += 1
                # if(m==cNum):
                #     return tmp
    return tmp

def noise_2D_vector_rect(n,m):

    noise = n*3/5
    real = n - noise

    import random
    ms = numpy.sqrt(2*m)
    if(ms>int(ms)):     # 向上取整
        ms = int(ms) + 1
    else:
        ms = int(ms)

    tmp = []
    count = 0
    c = int(real/m)
    if(c < float(real)/m): # 向上取整（没格的元素个数）
        c += 1

    w = real/(2*ms)
    # cNum = 0
    for i in range(ms):
        if(real==count):
            break

        for j in range(ms):
            if(real==count):
                break

            if((i%2)==(j%2)):
                pi0 = i*w
                pj0 = j*w
                pi1 = (i+1)*w
                pj1 = (j+1)*w
                ccount = 0
                while ccount<c:
                    if(real==count):
                            break
                    x = random.randint(pi0, pi1)
                    y = random.randint(pj0, pj1)
                    tu = (x,y)
                    if(tu not in tmp):
                        tmp.append(tu)
                        count += 1
                        ccount += 1
                        
                # cNum += 1
                # if(m==cNum):
                #     return tmp
    while count<n:
        x = random.randint(0, real/2)
        y = random.randint(0, real/2)
        tu = (x,y)
        # print tu
        if(tu not in tmp):
            tmp.append(tu)
            count += 1
            ccount += 1

    return tmp

'''   半随机生成大 n 个二维点样本， 属于 m 个类, 类以套环交替分布 '''
def rand_2D_vector_circle(n,m):

    import random
    cX = (2*m - 1)*10
    cY = (2*m - 1)*10

    total = 0
    for i in range(1,m+1):
        total += ((2*i-1)*(2*i-1))-((2*i-2)*(2*i-2))

    tmp = []
    count = 0
    for j in range(1,m+1):
        c = ((2*j-1)*(2*j-1))-((2*j-2)*(2*j-2))
        t = float(c)*n/total
        c = int (c*n/total)
        if(c<t):    # 向上取整
            c += 1

        Llimit = cX - (2*j-1)*10
        Hlimit = cX + (2*j-1)*10

        UP = ((2*j-1)*10)*((2*j-1)*10)
        DOWN = ((2*j-2)*10)*((2*j-2)*10)

        ccount = 0
        while ccount<c:
            x = random.randint(Llimit,Hlimit)
            y = random.randint(Llimit,Hlimit)
            r = (x-cX)*(x-cX)+(y-cY)*(y-cY)

            if (r<=UP and r>=DOWN):
                tu = (x,y)
                if(tu not in tmp):
                    tmp.append(tu)
                    count += 1

                    ccount += 1
                    # print count
                    if(n==count):
                        print "over"
                        return tmp 
    return tmp

def real_matrix ():
    matrix_path = "./pickle/matrix/Abby_Watkins.matrix"
    if not os.path.exists(matrix_path):
        print "./pickle/matrix/Abby_Watkins.matrix  ---- not exits"
        os.exits()

    matrix = load_matrix(matrix_path)
    return matrix