#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Construct a feature space vector and compute the similarity matrix.
"""

import math


class PersonCorpus(object):
    def __init__(self):
        self.vectors = []
        self.word_num = 0
        self.feature_freq = {}
        self.corpus_vector_num = 0
        self.corpus_feature_appear_vec_num = {}
        self.l2_norm = {}
        self.is_sorted = False
        self.is_tfidf = False

    def add_vector(self, vec):
        self.corpus_vector_num += 1
        vec.set_id(len(self.vectors))
        self.vectors.append(vec)
        self.word_num += vec.word_num()
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
            self.feature_freq[k] += self.feature_freq.get(k, 0) + v
            self.corpus_feature_appear_vec_num[k] += self.feature_freq.get(k, 0) + 1
        return None

    def get_matrix(self):
        if not self.is_sorted:
            self.sort()
        if not self.is_tfidf:
            self.complete_TFIDF()

        matrix = [[0.0] for i in range(len(self.feature_freq)) for j in range(len(self.vectors))]
        li = len(matrix)
        for i in range(li):
            vec = self.vectors[i]
            tfidf = vec.tfidf
            for f_no, fv in tfidf.items():
                matrix[i][f_no] = fv
        return matrix



class FeatureMapper(object):
# Use a dictionary using integer as keys to represent the feature name to accelerate the speed to computing.
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
    def __init__(self, features, feature_mapper, doc_meta,):
        self.feature_mapper = feature_mapper
        self.features = None
        self.vector = None
        self.features_to_vector(features)
        self.word_num = doc_meta['word_num']
        self.freq = None
        self.id = None
        self.tfidf = None

    def set_id(self, _id):
        self.id = _id
        return None

    def word_num(self):
        return self.word_num

    def features_to_vector(self, features):
        """
        @para: a dictionary of features like this:
        {feature_name_1: value_1, feature_name_2: value_2, ...}
        """
        vector = []
        fmapper = self.feature_mapper
        for fn, fv in features.items():
            f_no = fmapper.get(fn)
            if f_no is None:
                f_no = fmapper.add(fn)
            vector.append(f_no, fv)
            self.freq[f_no] = fv

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
            self.tfidf[w] = (self.freq[w] / float(self.word_num)) * \
                (math.log(corpus_vector_num /
                 float(corpus_feature_appear_vec_num[w]) + 1, 10))
        return None