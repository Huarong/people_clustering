#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lxml import etree
from readability.readability import Document

import util
from file_reader import FileReader


def text_extract(path, logger):
    with open(path) as f:
        html = f.read().strip()
        if not html:
            return ''
        doc = Document(html)
        try:
            summary = doc.summary()
        except:
            logger.info('extract summary failed: %s' % path)
            return ''
        root = etree.HTML(summary)
        content = ' '.join(root.xpath('string()').split())
    return content


def write_body(content, path):
    _dir = os.path.dirname(path)
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    with open(path, 'wb') as out:
        out.write(content.encode('utf-8'))
    return None


def main():
    logger = util.init_log('TextExtract', os.path.join(util.ROOT, 'log/text_extraction.log'), console=False)
    webpages_dir = os.path.join(util.ROOT, 'data/weps2007_data_1.1/traininig/web_pages')
    body_text_dir = os.path.join(util.ROOT, 'data/bodytext')
    if not os.path.exists(body_text_dir):
        os.mkdir(body_text_dir)

    for name in os.listdir(webpages_dir):
        logger.info('begin extract body text of %s' % name)
        reader = FileReader(webpages_dir, name)
        description = reader.read_description()
        for rank in description:
            html_path = os.path.join(webpages_dir, name, 'raw', rank, 'index.html')
            if not os.path.exists(html_path):
                logger.info('file path not exist: %s' % html_path)
                continue
            content = text_extract(html_path, logger)
            body_path = os.path.join(body_text_dir, name, '%s.txt' % rank)
            write_body(content, body_path)
    return None


if __name__ == '__main__':
    main()
