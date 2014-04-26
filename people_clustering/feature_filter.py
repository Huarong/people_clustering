#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import heapq

import util


class FeatureFilter(object):
    def __init__(self, threshold=100):
        self.threshold = threshold

    def filter(self, features, func=None):
        if func is None:
            func = lambda x: x[1]
        large = heapq.nlargest(self.threshold, features.items(), key=func)
        return dict(large)

    def filter_and_dump(self, feature_path, selected_path):
        with open(feature_path) as f1:
            features = json.load(f1)

        selected_features = {}
        for rank, v in features.items():
            feat = v[0]
            large = self.filter(feat)
            selected_features[rank] = large

        with open(selected_path, 'wb') as f2:
            json.dump(selected_features, f2)
        return None


def main():
    ff = FeatureFilter()
    feature_dir = os.path.join(util.ROOT, 'pickle/features/')
    selected_feature_dir = os.path.join(util.ROOT, 'pickle/selected_features/')
    if not os.path.exists(selected_feature_dir):
        os.makedirs(selected_feature_dir)

    for name in os.listdir(feature_dir):
        print 'begin %s' % name
        feature_path = os.path.join(feature_dir, name)
        selected_path = os.path.join(selected_feature_dir, name)
        ff.filter_and_dump(feature_path, selected_path)
    return None


if __name__ == '__main__':
    main()
