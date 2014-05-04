#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from lxml import etree
from readability.readability import Document
from nltk import clean_html

import util


def readability_extraction(html):
    doc = Document(html)
    summary = doc.summary()
    root = etree.HTML(summary)
    content = ' '.join(root.xpath('string()').split())
    return content


def ntlk_extraction(html):
    content = ' '.join(clean_html(html).split())
    return content


def text_extract(path, logger):
    with open(path) as f:
        html = f.read().strip().decode('utf-8', 'ignore')
        if not html:
            logger.info('NUll html file %s' % path)
            return ''
        # try:
        #     content = readability_extraction(html)
        #     # The result of body text extraction is not good enough
        #     if len(content) < 500:
        #         logger.info('Extract summary not good enough. Begin using NLTK with %s' % path)
        #         content = ntlk_extraction(html)
        #     else:
        #         logger.info('Success using readability with %s' % path)
        # except etree.XMLSyntaxError:
        #     logger.info('Extract summary failed. Begin using NLTK with %s' % path)
        content = ntlk_extraction(html)
    return content


def write_body(content, path, logger):
    _dir = os.path.dirname(path)
    util.makedir(_dir)
    with open(path, 'wb') as out:
        try:
            out.write(content.encode('utf-8'))
        except:
            logger.error('!!!!!! Invalid Encode with %s !!!!!!!' % path)
            out.write('Invalid HUO Encode')
    return None


@util.timer
def run(webpages_dir, body_text_dir, log_path):
    logger = util.init_log('TextExtract', log_path, console=False)
    util.makedir(body_text_dir)

    for name in os.listdir(webpages_dir):
        logger.info('begin extract body text of %s' % name)
        a_person_dir = os.path.join(webpages_dir, '%s/' % name)
        for file_name in os.listdir(a_person_dir):
            rank = file_name.split('.')[0]
            html_path = os.path.join(a_person_dir, file_name)
            content = text_extract(html_path, logger)
            body_path = os.path.join(body_text_dir, name, '%s.txt' % rank)
            write_body(content, body_path, logger)
    return None


def main():
    webpages_dir = os.path.join(util.ROOT, 'pickle/2008test/mapped_webpages_dir/')
    body_text_dir = os.path.join(util.ROOT, 'pickle/2008test/bodytext/')
    log_path = os.path.join(util.ROOT, 'log/2008test.nltk.log')
    run(webpages_dir, body_text_dir, log_path)
    return None


if __name__ == '__main__':
    main()
