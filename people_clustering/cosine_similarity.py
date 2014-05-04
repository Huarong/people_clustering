#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import unittest

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


def Euclidean_distance(a, b):
    distances = (a - b) ** 2
    distances = distances.sum(axis=-1)
    distances = numpy.sqrt(distances)
    return distances


def Euclidean_distance_similarity(matrix):
    length = len(matrix)
    sim_matrix = [[0.0 for j in range(length)] for i in range(length)]

    for i in range(length):
        row_i = matrix[i]
        for j in range(i + 1, length):
            sim_matrix[i][j] = 1.0 / (1.0 + Euclidean_distance(row_i, matrix[j]))
    return sim_matrix


def Jaccard(a, b):
    intersection = numpy.logical_and(a, b)
    union = numpy.logical_or(a, b)
    try:
        sim = float(intersection.sum()) / union.sum()
    except ZeroDivisionError:
        sim = 0.0
    return sim


def Jaccard_similarity(matrix):
    length = len(matrix)
    sim_matrix = [[0.0 for j in range(length)] for i in range(length)]
    for i in range(length):
        row_i = matrix[i]
        for j in range(i + 1, length):
            sim_matrix[i][j] = Jaccard(row_i, matrix[j])
    return sim_matrix


def compute_similarity(matrix):
    matrix = to_numpy_matrix(matrix)
    return Jaccard_similarity(matrix)


def run(matrix_dir, cosine_dir):
    util.makedir(cosine_dir)

    count = 0
    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        count += 1
        util.write('begin %s: %s' % (count, name))
        file_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(file_path)
        # sim_matrix = cosine(matrix)
        sim_matrix = compute_similarity(matrix)
        cosine_path = os.path.join(cosine_dir, '%s.matrix' % name)
        util.dump_matrix(sim_matrix, cosine_path)
    return None


class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_jaccard(self):
        a = [1, 3, 0, 0.12]
        b = [0, 2, 0, 200]
        target = 0.6666666666
        get = Jaccard(a, b)
        self.assertAlmostEqual(target, get)




def main():
    matrix_dir = util.abs_path('pickle/2008test/matrix')
    cosine_dir = util.abs_path('pickle/2008test/cosine/')
    run(matrix_dir, cosine_dir)
    return None



if __name__ == '__main__':
    # main()
    unittest.main()
