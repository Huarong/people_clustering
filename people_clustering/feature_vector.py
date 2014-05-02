#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a feature space vector and compute the similarity matrix.
"""

import os
import math

import util


class PersonCorpus(object):
    def __init__(self, name):
        self.name = name
        self.vectors = []
        self.feature_freq = {}
        self.corpus_feature_appear_vec_num = {}
        self.matrix = None

    def add_vector(self, vec):
        self.vectors.append(vec)
        self.update_freq(vec.freq)

    def complete_tfidf(self):
        vec_num = len(self.vectors)
        for vec in self.vectors:
            vec.compute_tfidf(vec_num, self.corpus_feature_appear_vec_num)
        return None

    def update_freq(self, freq):
        for k, v in freq.items():
            self.feature_freq[k] = self.feature_freq.get(k, 0) + v
            self.corpus_feature_appear_vec_num[k] = self.corpus_feature_appear_vec_num.get(k, 0) + 1
        return None

    def compute_matrix(self):
        self.vectors.sort(key=lambda x: x.id)
        self.complete_tfidf()

        li = len(self.vectors)
        lj = len(self.feature_freq)
        matrix = [[0.0 for j in range(lj)] for i in range(li)]
        for i in range(li):
            vec = self.vectors[i]
            for f_no, fv in vec.tfidf.items():
                matrix[i][f_no] = fv
        self.matrix = matrix
        print 'Finish computing matrix %s' % self.name
        print 'The matrix is %d * %d' % (li, lj)
        return None

    def dump_matrix(self, path):
        with open(path, 'wb') as out:
            for row in self.matrix:
                out.write(' '.join([str(e) for e in row]))
                out.write(os.linesep)
        print 'Finish writing matrix to %s' % path
        return None


class FeatureMapper(object):

    """
    Use a dictionary using integer as keys.
    Represent the feature name to accelerate the speed to computing.

    """

    def __init__(self):
        self.fmapper = {}

    def feature_mapper(self):
        return self.fmapper

    def get(self, fn):
        return self.fmapper.get(fn, None)

    def add(self, fn):
        f_no = len(self.fmapper)
        self.fmapper[fn] = f_no
        return f_no


class FeatureVector(object):
    def __init__(self, rank, features, feature_mapper):
        self.id = int(rank)
        self.feature_mapper = feature_mapper
        self.freq = {}
        self.largest_feature_count = 0
        self.tfidf = 0.0
        self.vector = None
        self.features_to_vector(features)

    def features_to_vector(self, features):
        """
        @para: a dictionary of features like this:
        {feature_name_1: count_1, feature_name_2: count_2, ...}
        """
        vector = []
        fmapper = self.feature_mapper
        largest_feature_count = 0

        for fn, fv in features.items():
            f_no = fmapper.get(fn)
            if f_no is None:
                f_no = fmapper.add(fn)
            vector.append((f_no, fv))
            self.freq[f_no] = fv

            if fv > largest_feature_count:
                largest_feature_count = fv

        self.largest_feature_count = largest_feature_count
        vector.sort()
        self.vector = vector
        return None

    def compute_tfidf(self, corpus_vector_num, corpus_feature_appear_vec_num):
        """
        Return a dict of Inverse Document Frequency.

        """
        tfidf = {}
        for w, c in self.freq.items():
            tfidf[w] = ((c / float(self.largest_feature_count)) *
                (math.log(corpus_vector_num /
                 float(corpus_feature_appear_vec_num[w]) + 1, 10)))
        self.tfidf = tfidf
        return None


def run(selected_feature_dir, matrix_dir):
    feature_dir = selected_feature_dir
    util.makedir(matrix_dir)

    for file_name in os.listdir(feature_dir):
        name = file_name.split('.')[0]
        feature_path = os.path.join(feature_dir, file_name)
        feature_dict = util.load_pickle(feature_path, typ='json')
        pc = PersonCorpus(name)
        fm = FeatureMapper()
        for rank, feat in feature_dict.items():
            vec = FeatureVector(rank, feat, fm)
            pc.add_vector(vec)
        pc.compute_matrix()
        matrix_path = os.path.join(matrix_dir, '%s.matrix' % name)
        pc.dump_matrix(matrix_path)
    return None


def main():
    selected_feature_dir = util.abs_path('pickle/2008test/selected_features/')
    matrix_dir = util.abs_path('pickle/2008test/matrix/')
    run(selected_feature_dir, matrix_dir)
    return None


if __name__ == '__main__':
    main()
