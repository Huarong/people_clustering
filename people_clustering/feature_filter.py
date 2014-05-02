#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import heapq

import util


class FeatureFilter(object):
    def __init__(self, threshold=500):
        self.threshold = threshold

    def filter(self, features, func=None):
        # if features length is not longer than threshold, return all the features
        if len(features) <= self.threshold:
            return features
        if func is None:
            func = lambda x: x[1]
        large = heapq.nlargest(self.threshold, features.items(), key=func)
        return dict(large)

    def filter_and_dump(self, feature_path, selected_path):
        features = util.load_pickle(feature_path, typ='json')
        selected_features = {}

        for rank, v in features.items():
            feat = v[0]
            large = self.filter(feat)
            selected_features[rank] = large

        util.pickle_me(selected_features, selected_path, typ='json')
        return None


def run(feature_dir, selected_feature_dir):
    ff = FeatureFilter()
    util.makedir(selected_feature_dir)

    for name in os.listdir(feature_dir):
        util.write('begin %s' % name)
        feature_path = os.path.join(feature_dir, name)
        selected_path = os.path.join(selected_feature_dir, name)
        ff.filter_and_dump(feature_path, selected_path)
    return None


def main():
    feature_dir = util.abs_path('pickle/2008test/features/')
    selected_feature_dir = util.abs_path('pickle/2008test/selected_features/')
    run(feature_dir, selected_feature_dir)
    return None


if __name__ == '__main__':
    main()
