#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle as pickle

import numpy as np

import util

from people_clustering.mycluster.gaac import GAAClusterer


def main():
    matrix_dir = os.path.join(util.ROOT, 'pickle/svd_matrix/')
    category_dir = os.path.join(util.ROOT, 'pickle/category/')
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    clusterer = GAAClusterer()
    count = 0
    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        count += 1
        print 'begin %s: %s' % (count, name)
        file_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(file_path)
        print '--------------'
        print len(matrix)
        np_matrix = [np.array(row) for row in matrix]
        print np_matrix
        result = clusterer.cluster(np_matrix, False, "euc", "mean")
        category_path = os.path.join(category_dir, '%s.pickle' % name)
        with open(category_path, 'wb') as fp:
            pickle.dump(result, fp)
    return None


if __name__ == '__main__':
    main()
