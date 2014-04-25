#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from __init__ import ROOT

from people_clustering.stopword_filter import StopwordFilter


class TestStopwordFilter(unittest.TestCase):
    def setUp(self):
        self.swf = StopwordFilter()

    def test_filter(self):
        tokens = [(u'risk', 108), (u'be', 72), (u'was', 64), (u'profit', 59), (u'market', 41), (u'had', 38), (u'trading', 36), (u'were', 36)]
        print tokens
        got = self.swf.filter(tokens)
        target = [(u'risk', 108), (u'profit', 59), (u'market', 41), (u'had', 38), (u'trading', 36)]
        self.assertListEqual(target, got)

if __name__ == '__main__':
    unittest.main()
