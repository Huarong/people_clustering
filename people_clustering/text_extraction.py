#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lxml import etree
from readability.readability import Document


def text_extract(path):
    with open(path) as f:
        html = f.read()
        doc = Document(html)
        summary = doc.summary()
        root = etree.HTML(summary)
        # content = ''.join(root.xpath('.//text()'))
        content = ' '.join(root.xpath('string()').split())
    return content
