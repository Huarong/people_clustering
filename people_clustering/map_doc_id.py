#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

import util


class DocidMapper(object):
    def __init__(self, name, doc_dir, mapped_webpages_dir, id_mapper_pickle_dir,):
        self.name = name
        self.doc_dir = doc_dir
        self.mapped_webpages_dir = mapped_webpages_dir
        self.id_mapper_pickle_dir = id_mapper_pickle_dir
        # map from docid to continue number 0, 1, 2, ...
        self.id_mapper = {}
        # a list storing docid the index mapped
        self.inverted_id_mapper_list = []

    def mv(self, mapped_doc_dir):
        id_mapper = self.id_mapper
        util.makedir(mapped_doc_dir)
        for file_name in os.listdir(self.doc_dir):
            source_path = os.path.join(self.doc_dir, file_name)
            doc_id = file_name.split('.')[0]
            mapped_doc_id = id_mapper[doc_id]
            mapped_file_name = str(mapped_doc_id).zfill(3) + '.html'
            target_path = os.path.join(self.mapped_webpages_dir, mapped_doc_dir, mapped_file_name)
            cmd = ['cp', source_path, target_path]
            subprocess.call(cmd)
        return None

    def build(self):
        id_mapper_dir = self.id_mapper_pickle_dir
        id_mapper = {}
        for file_name in os.listdir(self.doc_dir):
            doc_id = file_name.split('.')[0]
            id_mapper[doc_id] = len(id_mapper)
        self.id_mapper = id_mapper

        inverted_id_mapper_list = ['' for i in range(len(id_mapper))]
        for k, v in id_mapper.items():
            inverted_id_mapper_list[v] = k
        self.inverted_id_mapper_list = inverted_id_mapper_list

        id_mapper_path = os.path.join(id_mapper_dir, '%s.json' % self.name)
        inverted_id_mapper_list_path = os.path.join(id_mapper_dir, '%s.inv.pickle' % self.name)
        util.pickle_me(id_mapper, id_mapper_path, typ='json')
        util.pickle_me(inverted_id_mapper_list, inverted_id_mapper_list_path)
        return None

    def run(self):
        self.build()
        mapped_doc_dir = os.path.join(self.mapped_webpages_dir, '%s/' % self.name)
        self.mv(mapped_doc_dir)



def run(webpages_dir, mapped_webpages_dir, id_mapper_pickle_dir):
    for name in os.listdir(webpages_dir):
        print '--------------------- %s ---------------' % name
        doc_dir = os.path.join(webpages_dir, '%s/' % name)
        dm = DocidMapper(name, doc_dir, mapped_webpages_dir, id_mapper_pickle_dir)
        dm.run()
        del dm
    return None


def main():
    webpages_dir = 'data/weps-2/data/test/web_pages'
    mapped_webpages_dir = 'pickle/2008test/mapped_webpages_dir/'
    id_mapper_pickle_dir = 'pickle/2008test/id_mapper/'
    run(webpages_dir, mapped_webpages_dir, id_mapper_pickle_dir)


if __name__ == '__main__':
    main()
