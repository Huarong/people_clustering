#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pickle

import networkx as nx
import community

import util


class Louvain(object):
    def __init__(self):
        self.G = None

    def load_graph(self, path):
        matrix = util.load_matrix(path)
        G = nx.Graph()
        length = len(matrix)
        for i in range(length):
            edges_list = [(i, j, matrix[i][j]) for j in range(i+1, length)]
            G.add_weighted_edges_from(edges_list)
        self.G = G
        return None

    def cluster(self):
        #first compute the best partition
        partition = community.best_partition(self.G)
        # print partition
        category = [(c,) for i, c in partition.items()]
        # print category
        return category


def run(cosine_dir, category_dir):
    cosine_dir = os.path.join(util.ROOT, 'pickle/cosine/')
    category_dir = os.path.join(util.ROOT, 'pickle/category/')
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    count = 0
    for file_name in os.listdir(cosine_dir):
        name = file_name.split('.')[0]
        count += 1
        print 'begin %s: %s' % (count, name)
        file_path = os.path.join(cosine_dir, file_name)
        lou = Louvain()
        lou.load_graph(file_path)
        try:
            category = lou.cluster()
            del lou
        except:
            print '------------- %s ----------' % name
            continue
        category_path = os.path.join(category_dir, '%s.pickle' % name)
        with open(category_path, 'wb') as fp:
            pickle.dump(category, fp)
        # if count > 2:
        #     break
    return None


def main():
    cosine_dir = util.abs_path('pickle/2008test/cosine/')
    category_dir = util.abs_path('pickle/2008test/category/')
    run(cosine_dir, category_dir)
    return None


if __name__ == '__main__':
    main()
