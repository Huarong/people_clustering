#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import util

from file_reader import FileReader
from text_extraction import extract


def main():
    webpages_dir = os.path.join(util.ROOT, 'data/weps2007_data_1.1/traininig/web_pages')
    for name in os.listdir(webpages_dir):
        reader = FileReader(webpages_dir, name)
        description = reader.read_description()
        for rank in description:
            html_path = os.path.join(webpages_dir, name, 'raw', rank, 'index.html')
            summary = extract(html_path)
            print summary.encode('utf-8')
            break
        break


if __name__ == '__main__':
    main()