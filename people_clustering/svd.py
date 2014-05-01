#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import numpy as np

import util


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


def run(matrix_dir, svd_matrix_dir):
    if not os.path.exists(svd_matrix_dir):
        os.makedirs(svd_matrix_dir)

    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        matrix_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(matrix_path)
        svd_matrix = get_topicMatrix(np.array(matrix), len(matrix))
        svd_path = os.path.join(svd_matrix_dir, '%s.matrix' % name)
        util.dump_matrix(svd_matrix, svd_path)
    return None


def main():
    matrix_dir = util.abs_path('pickle/2008test/matrix/')
    svd_matrix_dir = util.abs_path('pickle/2008test/svd_matrix/')
    run(matrix_dir, svd_matrix_dir)
    return None


if __name__ == '__main__':
    # test_get_topicMatrix()
    main()
