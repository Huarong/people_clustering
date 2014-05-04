#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

from lxml import etree

import util


class BackMapper(object):
    def __init__(self, name, inverted_mapper_dir, before_map_back_result_dir, result_dir, config):
        self.name = name
        self.inverted_mapper_dir = inverted_mapper_dir
        self.before_map_back_result_dir = before_map_back_result_dir
        self.result_dir = result_dir
        self.result_file_extension = config['result_file_extension']
        self.inverted_id_mapper_list = []
        self.exit = False

    def read_mapper(self):
        path = os.path.join(self.inverted_mapper_dir, '%s.inv.pickle' % self.name)
        try:
            self.inverted_id_mapper_list = util.load_pickle(path)
        except EOFError, e:
            print e
            print '!!!!! Fail to read inverted id map of %s' % self.name
            self.exit = True
        return None

    def convert(self):
        path = os.path.join(self.before_map_back_result_dir, '%s.%s' % (self.name, self.result_file_extension))
        print path
        with open(path) as f:
            root = etree.XML(f.read())
        entities = root.xpath('./entity') + root.xpath('./discarded')
        for entity in entities:
            for doc in entity:
                rank = doc.get('rank')
                real_rank = self.inverted_id_mapper_list[int(rank)]
                # remove the heading zero in rank like 012 ==> 12
                real_rank = real_rank.lstrip('0')
                doc.set('rank', real_rank)

        xml = etree.ElementTree(root)
        out_path = os.path.join(self.result_dir, '%s.%s' % (self.name, self.result_file_extension))
        with open(out_path, 'wb') as out:
            xml.write(out, xml_declaration=True, encoding='utf-8')
        return None

    def run(self):
        self.read_mapper()
        if self.exit:
            return None
        else:
            self.convert()
        return None


def run(inverted_mapper_dir, before_map_back_result_dir, result_dir, config):
    for file_name in os.listdir(before_map_back_result_dir):
        name = file_name.split('.')[0]
        print '--------------------- %s ---------------' % name
        bm = BackMapper(name, inverted_mapper_dir, before_map_back_result_dir, result_dir, config)
        bm.run()
        del bm
    return None


def main():
    inverted_mapper_dir = 'pickle/2008test/id_mapper/'
    before_map_back_result_dir = 'pickle/2008test/before_map_back_result/louvain'
    result_dir = 'pickle/2008test/result/louvain'
    run(inverted_mapper_dir, before_map_back_result_dir, result_dir)
    return None


if __name__ == '__main__':
    main()
