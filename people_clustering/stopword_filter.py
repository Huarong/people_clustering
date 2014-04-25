#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import copy

import util


class StopwordFilter(object):
    def __init__(self, path=None):
        if path is None:
            self.stopword_path = os.path.join(util.ROOT, 'dict/stopword.txt')
        else:
            self.stopword_path = path
        self.stopwords = None
        self.load_stopword()

    def load_stopword(self):
        with open(self.stopword_path) as f:
            self.stopwords = set([line.strip() for line in f.readlines()])
        return None

    def filter(self, features):
        f = {}
        for k, v in features.items():
            if k not in self.stopwords:
                f[k] = v
        return f
