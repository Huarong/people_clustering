#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from lxml import etree


class FileReader(object):
    def __init__(self, webpages_dir, name):
        self.webpages_dir = webpages_dir
        self.description = {}
        self.name = name

    def get_description(self):
        return self.description

    def read_webpages(self):
        self.read_description()
        return None

    def read_description(self):
        xml_path = os.path.join(self.webpages_dir, self.name, '%s.xml' % self.name)
        with open(xml_path) as page:
            root = etree.XML(page.read())
            docs = root.xpath('./doc')
            for d in docs:
                rank = d.get('rank').zfill(3)
                url = d.get('url')
                self.description[rank] = {'url': url}
        return self.description
