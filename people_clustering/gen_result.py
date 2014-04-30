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
            for ei in e:
                entities[ei].append(i)
        self.entities = entities

    def dump_xml(self, path):
        name = self.name.replace('_', ' ')
        clustering = etree.Element('clustering', name=name)
        xml = etree.ElementTree(clustering)
        for entity_id, doc_ranks in self.entities.items():
            entity_element = etree.SubElement(clustering, 'entity', id=str(entity_id))
            for rank in doc_ranks:
                doc_element = etree.SubElement(entity_element, 'doc', rank=str(rank))
        with open(path, 'wb') as out:
            xml.write(out, xml_declaration=True, encoding='utf-8')
        return None


def run(category_dir, result_dir):
    category_dir = os.path.join(util.ROOT, 'pickle/category/')
    result_dir = os.path.join(util.ROOT, 'result/myresult/nineH')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    for file_name in os.listdir(category_dir):
        name = file_name.split('.')[0]
        category_path = os.path.join(category_dir, file_name)
        with open(category_path) as f:
            category = pickle.load(f)
        ps = PeopleSet(name, category)
        clustering_result_path = os.path.join(result_dir, '%s.clust.xml' % name)
        ps.dump_xml(clustering_result_path)
        del ps
    return None


def main():
    category_dir = util.abs_path('pickle/2008test/louvain_category/')
    result_dir = util.abs_path('pickle/2008test/result/louvain')
    run(category_dir, result_dir)
    return None


if __name__ == '__main__':
    main()
