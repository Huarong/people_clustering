#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle as pickle

import numpy as np

import util

from people_clustering.mycluster_nltk.AD_Cluster import AD_Cluster
from people_clustering.mycluster_nltk.DeNoise import cutNoise


def run(matrix_dir, category_dir):

    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    clusterer = AD_Cluster()
    count = 0
    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        count += 1
        print 'begin %s: %s' % (count, name)
        file_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(file_path)

        size = len(matrix)
        result = [(9999,)]*size    # 9999 号类表示 discard， 初始默认所有样本为 discard 状态
        realPTs, noisePTs,tmp,angles,real,noise= cutNoise(matrix)
        print "len of real",len(real)
        print "len of realPTs",len(realPTs)
        # --------------------噪声自成一类-------------------------
        cNum = 0        # 记录已使用类标签数量
        for i in noise:
            result[i] = (cNum,)
            cNum += 1
        # -------------------------------------------------------
        np_matrix = [np.array(row) for row in realPTs]
        print np_matrix
        result0 = clusterer.cluster(np_matrix, False,None, "euc", "mean")

        print "len of result0",len(result0)
        
        print "len of result",len(result)
        # ---------------- 聚类结果标签加上原来已用的类标数 ----------
        for i, c in enumerate(result0): 
             result[real[i]] = (c[0] + cNum,)

        category_path = os.path.join(category_dir, '%s.pickle' % name)
        with open(category_path, 'wb') as fp:
            pickle.dump(result, fp)

        # if count > 5:
        #      break
    return None


def main():
    matrix_dir = os.path.join(util.ROOT, 'pickle/2008test/matrix/')
    category_dir = os.path.join(util.ROOT, 'pickle/2008test/category/nltk')
    run(matrix_dir, category_dir)
    return None


if __name__ == '__main__':
    main()
