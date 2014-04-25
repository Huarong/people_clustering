#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print ROOT

def get_topicMatrix(Matrix, topicNum, fill = True):
    h,w = Matrix.shape
    if(True==fill):
        add = float(np.sum(Matrix))/(h*w)
        tmp = np.zeros((h,w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                if(0==Matrix[i][j]):
                    tmp[i][j] += add
                else:
                    tmp[i][j] += float(Matrix[i][j])
        Matrix = tmp
    m = min(h,w)
    if (m<topicNum):
        print "topicNum is large than the minor dimension of the Matrix!"
        sys.exist()
    u,s,v = np.linalg.svd(Matrix)
    l = len(s)
    sm = np.zeros((l,l))
    for i in range(topicNum):
        sm[i][i] = s[i]

    if(h<w):
        Matrix2 = (u.dot(sm)).dot(v[0:h,0:w])
    else:
        Matrix2 = (u[0:h,0:w].dot(sm)).dot(v)

    return Matrix2

def test_get_topicMatrix():
    n = np.array([[4, 3, 2, 1, 0],[0, 3, 2, 1, 0],[4, 4, 2, 7, 0],[1, 0, 0, 0, 0],[0, 0, 0, 1, 1]])
    tm = get_topicMatrix(n, 2,False)
    print tm


if __name__=="__main__":
	test_get_topicMatrix()