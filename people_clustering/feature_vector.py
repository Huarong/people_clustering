#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a feature space vector and compute the similarity matrix.
"""

import os
import math
import time
import json

import util


class PersonCorpus(object):
    def __init__(self, name):
        self.name = name
        self.vectors = []
        self.feature_freq = {}
        self.corpus_vector_num = 0
        self.corpus_feature_appear_vec_num = {}
        self.l2_norm = {}
        self.is_sorted = False
        self.is_tfidf = False
        self.matrix = None

    def add_vector(self, vec):
        self.corpus_vector_num += 1
        vec.set_id(len(self.vectors))
        self.vectors.append(vec)
        self.update_freq(vec.freq)

    def complete_TFIDF(self):
        for vec in self.vectors:
            vec.compute_TFIDF(self.corpus_vector_num, self.corpus_feature_appear_vec_num)
        return None

    def sort(self):
        self.vectors.sort(key=lambda x: x.id)
        self.is_sorted = True
        return None

    def update_freq(self, freq):
        for k, v in freq.items():
            self.feature_freq[k] = self.feature_freq.get(k, 0) + v
            self.corpus_feature_appear_vec_num[k] = self.corpus_feature_appear_vec_num.get(k, 0) + 1
        return None

    def compute_matrix(self):
        if not self.is_sorted:
            self.sort()
        if not self.is_tfidf:
            self.complete_TFIDF()

        li = len(self.vectors)
        lj = len(self.feature_freq)
        matrix = [[0.0 for j in range(lj)] for i in range(li)]
        for i in range(li):
            vec = self.vectors[i]
            tfidf = vec.tfidf
            for f_no, fv in tfidf.items():
                matrix[i][f_no] = fv
        self.matrix = matrix
        print 'Finish computing matrix %s' % self.name
        print 'The matrix is %d * %d' % (li, lj)
        return None

    def get_matrix(self):
        return self.matrix

    def dump_matrix(self, path=None):
        if path is None:
            tmp_path = os.path.join(util.ROOT, 'tmp')
            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
            path = os.path.join(tmp_path, '%s.matrix' % self.name)

        with open(path, 'wb') as out:
            for row in self.matrix:
                out.write(' '.join([str(e) for e in row]))
                out.write(os.linesep)
        print 'Finish writing matrix to %s' % path
        return None



class FeatureMapper(object):
    # Use a dictionary using integer as keys
    # to represent the feature name to accelerate the speed to computing.
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
    def __init__(self, features, feature_mapper):
        self.feature_mapper = feature_mapper
        self.features = None
        self.vector = None
        self.freq = {}
        self.largest_feature_count = 0
        self.id = None
        self.tfidf = None
        self.features_to_vector(features)


    def set_id(self, _id):
        self.id = _id
        return None

    def features_to_vector(self, features):
        """
        @para: a dictionary of features like this:
        {feature_name_1: value_1, feature_name_2: value_2, ...}
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

    def __mul__(self, other):
        """
        Overwrite the a * b method.
        Return the inner production of two FeatureVector object.
        """
        product = 0.0
        la = len(self.vector)
        lb = len(other.vector)
        i = 0
        j = 0
        while i < la and j < lb:
            ai = self.vector[i]
            bj = other.vector[j]
            ai_key = ai[0]
            bj_key = bj[0]
            if ai_key == bj_key:
                product += ai[1] * bj[1]
                i += 1
                j += 1
            elif ai_key < bj_key:
                i += 1
            else:
                j += 1
        return product

    def l2_norm(self):
        accumulation = 0.0
        for e in self.vector.values():
            accumulation += e * e
        norm = math.sqrt(accumulation)
        return norm

    def compute_TFIDF(self, corpus_vector_num, corpus_feature_appear_vec_num):
        """
        Return a dict of Inverse Document Frequency.

        """
        self.tfidf = {}
        for w in self.freq:
            self.tfidf[w] = (self.freq[w] / float(self.largest_feature_count)) * \
                (math.log(corpus_vector_num /
                 float(corpus_feature_appear_vec_num[w]) + 1, 10))
        return None


def main():
    feature_dir = os.path.join(util.ROOT, 'pickle/selected_features/')
    matrix_dir = os.path.join(util.ROOT, 'pickle/matrix/')
    if not os.path.exists(matrix_dir):
        os.makedirs(matrix_dir)

    for file_name in os.listdir(feature_dir):
        name = file_name.split('.')[0]
        feature_path = os.path.join(feature_dir, file_name)
        with open(feature_path) as fp:
            feature_dict = json.load(fp)
        pc = PersonCorpus(name)
        fm = FeatureMapper()
        for rank, feat in feature_dict.items():
            vec = FeatureVector(feat, fm)
            pc.add_vector(vec)
        pc.compute_matrix()
        matrix_path = os.path.join(matrix_dir, '%s.matrix' % name)
        pc.dump_matrix(path=matrix_path)
    return None


if __name__ == '__main__':
    main()
