#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import sys

import numpy

import util


def compute_L2_norm_list(matrix):
    length = len(matrix)
    L2_norms = [0.0 for i in range(length)]
    for i, row in enumerate(matrix):
        L2_norms[i] = math.sqrt(numpy.dot(row, row))
    return L2_norms


def to_numpy_matrix(matrix):
    return [numpy.array(row) for row in matrix]


def cosine(matrix):
    length = len(matrix)
    matrix = to_numpy_matrix(matrix)

    L2_norms = compute_L2_norm_list(matrix)
    sim_matrix = [[0.0 for j in range(length)] for i in range(length)]

    for i in range(length):
        for j in range(i + 1, length):
            inner_prod = numpy.dot(matrix[i], matrix[j])
            if inner_prod == 0.0:
                continue
            else:
                sim_matrix[i][j] = inner_prod / (L2_norms[i] * L2_norms[j])
    return sim_matrix


def run(matrix_dir, cosine_dir):
    util.makedir(cosine_dir)

    count = 0
    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        count += 1
        util.write('begin %s: %s' % (count, name))
        file_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(file_path)
        sim_matrix = cosine(matrix)
        cosine_path = os.path.join(cosine_dir, '%s.matrix' % name)
        util.dump_matrix(sim_matrix, cosine_path)
    return None


def main():
    matrix_dir = util.abs_path('pickle/2008test/matrix')
    cosine_dir = util.abs_path('pickle/2008test/cosine/')
    run(matrix_dir, cosine_dir)
    return None



if __name__ == '__main__':
    main()
