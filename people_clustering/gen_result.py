#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import cPickle as pickle
from collections import defaultdict

from lxml import etree

import util

class PeopleSet(object):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.entities = None
        self.gather_entity()

    def gather_entity(self):
        entities = defaultdict(list)
        for i, e in enumerate(self.category):
            entities[e].append(i)
        self.entities = entities

    def dump_xml(self, path):
        clustering = etree.Element('clustering', name=self.name)
        xml = etree.ElementTree(clustering)
        for entity_id, doc_ranks in self.entities.items():
            entity_element = etree.SubElement(clustering, 'entity', id=str(entity_id))
            for rank in doc_ranks:
                doc_element = etree.SubElement(entity_element, 'doc', rank=str(rank))
        with open(path, 'wb') as out:
            xml.write(out, xml_declaration=True, encoding='utf-8')
        return None


def main():
    category_dir = os.path.join(util.ROOT, 'pickle/category/')
    clustering_result_dir = os.path.join(util.ROOT, 'result/')
    if not os.path.exists(category_dir):
        os.makedirs(category_dir)

    for file_name in os.listdir(category_dir):
        name = file_name.split('.')[0]
        category_path = os.path.join(category_dir, file_name)
        category = pickle.load(category_path)
        ps = PeopleSet(name, category)
        clustering_result_path = os.path.join(clustering_result_dir, '%s.xml' % name)
        ps.dump_xml(clustering_result_path)
        del ps
    return None


if __name__ == '__main__':
    main()
