#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import util


class DocidMapper(object):
    def __init__(self, name, doc_dir, mapped_webpages_dir, id_mapper_pickle_dir, config):
        self.name = name
        self.version = config['version']
        self.doc_dir = doc_dir
        self.mapped_webpages_dir = mapped_webpages_dir
        self.id_mapper_pickle_dir = id_mapper_pickle_dir
        # map from docid to continue number 0, 1, 2, ...
        self.id_mapper = {}
        # a list storing docid the index mapped
        self.inverted_id_mapper_list = []

    def cp(self, mapped_doc_dir):
        id_mapper = self.id_mapper
        util.makedir(mapped_doc_dir)
        for file_name in os.listdir(self.doc_dir):
            if self.version == '2007test':
                source_path = os.path.join(self.doc_dir, file_name, 'index.html')
            elif self.version == '2008test':
                source_path = os.path.join(self.doc_dir, file_name)
            print source_path
            doc_id = file_name.split('.')[0].lstrip('0').zfill(1)
            mapped_doc_id = id_mapper[doc_id]
            mapped_file_name = '%d.html' % mapped_doc_id
            target_path = os.path.join(mapped_doc_dir, mapped_file_name)
            cmd = ['cp', source_path, target_path]
            util.write('Copy file from %s to %s' % (source_path, target_path))
            subprocess.call(cmd)
        return None

    def build(self):
        id_mapper_dir = self.id_mapper_pickle_dir
        id_mapper = {}
        for file_name in os.listdir(self.doc_dir):
            if self.version == '2007test':
                doc_id = file_name.lstrip('0').zfill(1)
            elif self.version == '2008test':
                doc_id = file_name.split('.')[0].lstrip('0').zfill(1)
            else:
                raise Exception('Invalid version: %s' % self.version)
            id_mapper[doc_id] = len(id_mapper)
        self.id_mapper = id_mapper

        self.inverted_id_mapper_list = [k for k, v in sorted(id_mapper.items(), key=lambda x: x[1])]

        id_mapper_path = os.path.join(id_mapper_dir, '%s.json' % self.name)
        inverted_id_mapper_list_path = os.path.join(id_mapper_dir, '%s.inv.pickle' % self.name)
        util.pickle_me(self.id_mapper, id_mapper_path, typ='json')
        util.pickle_me(self.inverted_id_mapper_list, inverted_id_mapper_list_path)
        return None

    def run(self):
        self.build()
        mapped_doc_dir = os.path.join(self.mapped_webpages_dir, '%s/' % self.name)
        self.cp(mapped_doc_dir)


def run(webpages_dir, mapped_webpages_dir, id_mapper_pickle_dir, config):
    version = config['version']
    for name in os.listdir(webpages_dir):
        print '--------------------- %s ---------------' % name
        if version == '2007test':
            doc_dir = os.path.join(webpages_dir, '%s/' % name, 'raw')
        elif version == '2008test':
            doc_dir = os.path.join(webpages_dir, '%s/' % name)
        else:
            raise Exception('Invalid version: %s' % version)
        print doc_dir
        dm = DocidMapper(name, doc_dir, mapped_webpages_dir, id_mapper_pickle_dir, config)
        dm.run()
        del dm
    return None


def main():
    webpages_dir = os.path.join(util.ROOT, 'data/weps-2/data/test/web_pages')
    mapped_webpages_dir = os.path.join(util.ROOT, 'pickle/2008test/mapped_webpages_dir/')
    id_mapper_pickle_dir = os.path.join(util.ROOT, 'pickle/2008test/id_mapper/')
    run(webpages_dir, mapped_webpages_dir, id_mapper_pickle_dir)


if __name__ == '__main__':
    main()
