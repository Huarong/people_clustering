#!/usr/bin/env python
# -*- coding: utf-8 -*-

import heapq

import util


class FeatureFilter(object):
    def __init__(self, threshold=100):
        self.threshold = threshold

    def filter(self, features, func=None):
        if func is None:
            func = lambda x: x[1]
        large = heapq.nlargest(self.threshold, features.items(), key=func)
        return large
