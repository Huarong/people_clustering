#!/usr/bin/env python
# -*- coding: utf-8 -*-

import util


class FeatureFilter(object):
    def __init__(self, threshold=100):
        self.threshold = threshold

    def filter(self, tokens, func=None):
        if func is None:
            func = lambda x: x[1]
        tokens.sort(key=func, reverse=True)[:self.threshold]
        return tokens
