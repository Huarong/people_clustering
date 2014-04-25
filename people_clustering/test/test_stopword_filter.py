#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from __init__ import ROOT

from people_clustering.stopword_filter import StopwordFilter


class TestStopwordFilter(unittest.TestCase):
    def setUp(self):
        self.swf = StopwordFilter()

    def test_filter(self):
        features = {u'be': 72, u'risk': 108, u'profit': 59, u'had': 38, u'trading': 36, u'were': 36, u'was': 64, u'market': 41}
        got = self.swf.filter(features)
        target = {u'profit': 59, u'had': 38, u'trading': 36, u'risk': 108, u'market': 41}
        self.assertDictEqual(target, got)

if __name__ == '__main__':
    unittest.main()
