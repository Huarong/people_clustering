#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import util

from file_reader import FileReader
from text_extraction import extract
from Filter_test import Filter
from stopword_filter import StopwordFilter
from feature_filter import FeatureFilter


def main():
    webpages_dir = os.path.join(util.ROOT, 'data/weps2007_data_1.1/traininig/web_pages')
    flt = Filter()
    ff = FeatureFilter()
    swf = StopwordFilter()
    for name in os.listdir(webpages_dir):
        reader = FileReader(webpages_dir, name)
        description = reader.read_description()
        for rank in description:
            html_path = os.path.join(webpages_dir, name, 'raw', rank, 'index.html')
            content = extract(html_path)
            features = flt.filt(content)
            good_features = ff.filter(features)
            print good_features
            break
        break


if __name__ == '__main__':
    main()