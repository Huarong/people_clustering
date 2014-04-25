#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

sys.path.insert(0, ROOT)

from people_clustering.text_extraction import text_extract


class TestTextExtraction(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_extract(self):
        global ROOT
        path = os.path.join(ROOT, 'data/weps2007_data_1.1/traininig/web_pages/Abby_Watkins/raw/002/index.html')
        summary = text_extract(path)
        with open('Abby_Watkins.summary') as f:
            target = f.read().decode('utf-8')
        self.assertMultiLineEqual(target, summary)

if __name__ == '__main__':
    unittest.main()
