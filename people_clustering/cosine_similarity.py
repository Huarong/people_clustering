#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math

import numpy

import util


def inner_production(a, b):
    ip = 0.0
    assert len(a) == len(b)
    for i in range(len(a)):
        ip += a[i] * b[i]
    return ip


def L2_norm(seq):
    # for loop is much faster sum(sequence) and np.sum(not_numpy_array_sequence)
    accumulation = 0.0
    for v in seq:
        accumulation += v * v
    norm = math.sqrt(accumulation)
    return norm


def compute_inner_product_matrix(matrix):
    length = len(matrix)
    inner_prod_matrix = [[0.0 for i in range(length)] for j in range(length)]
    for i in range(length):
        for j in range(i + 1, length):
            inner_prod_matrix[i][j] = inner_production(matrix[i], matrix[j])
    return inner_prod_matrix


def compute_L2_norm_list(matrix):
    length = len(matrix)
    L2_norm_list = [0.0 for i in range(length)]
    for i in range(length):
        L2_norm_list[i] = L2_norm(matrix[i])
    return L2_norm_list


def cosine_distance(u, v):      # cos():为相似性， 1-cos():为相似性距离
    """
    Returns 1 minus the cosine of the angle between vectors v and u. This is equal to
    1 - (u.v / |u||v|).
    """
    return numpy.dot(u, v) / (math.sqrt(numpy.dot(u, u)) * math.sqrt(numpy.dot(v, v)))


def cosine(matrix):
    length = len(matrix)
    sim_matrix = [[0.0 for i in range(length)] for j in range(length)]
    for i in range(length):
        for j in range(i + 1, length):
            sim_matrix[i][j] = cosine_distance(matrix[i], matrix[j])
    return sim_matrix


def run(matrix_dir, cosine_dir):
    if not os.path.exists(cosine_dir):
        os.makedirs(cosine_dir)

    count = 0
    for file_name in os.listdir(matrix_dir):
        name = file_name.split('.')[0]
        count += 1
        print 'begin %s: %s' % (count, name)
        file_path = os.path.join(matrix_dir, file_name)
        matrix = util.load_matrix(file_path)
        sim_matrix = cosine(matrix)
        cosine_path = os.path.join(cosine_dir, '%s.matrix' % name)
        util.dump_matrix(sim_matrix, cosine_path)
    return None


def main():
    matrix_dir = util.abs_path('pickle/2008test/svd_matrix')
    cosine_dir = util.abs_path('pickle/2008test/cosine/')
    run(matrix_dir, cosine_dir)
    return None



if __name__ == '__main__':
    main()
