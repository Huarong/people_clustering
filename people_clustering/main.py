#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import util

from file_reader import FileReader
from text_extraction import text_extract
from FeatureExtractor import FeatureExtractor
from feature_filter import FeatureFilter
from feature_vector import PersonCorpus, FeatureMapper, FeatureVector


@util.timer
def main():
    webpages_dir = os.path.join(util.ROOT, 'data/weps2007_data_1.1/traininig/web_pages')
    fe = FeatureExtractor()
    ff = FeatureFilter()
    for name in os.listdir(webpages_dir):
        print 'begin clustering %s' % name
        reader = FileReader(webpages_dir, name)
        description = reader.read_description()
        pc = PersonCorpus(name)
        fm = FeatureMapper()
        for rank in description:
            doc_meta = {}
            html_path = os.path.join(webpages_dir, name, 'raw', rank, 'index.html')
            content = text_extract(html_path)
            features, wordcount = fe.extract(content)
            doc_meta['word_num'] = wordcount
            good_features = ff.filter(features)
            vec = FeatureVector(good_features, fm)
            pc.add_vector(vec)
        pc.compute_matrix()
        pc.dump_matrix()


if __name__ == '__main__':
    main()