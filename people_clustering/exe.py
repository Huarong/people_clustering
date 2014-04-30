#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import argparse
from collections import OrderedDict

import util
import map_doc_id
import text_extraction
import FeatureExtractor
import feature_filter
import feature_vector
import svd
import cosine_similarity
import louvain
import gen_result
import map_back


class Task(object):
    def __init__(self, config):
        self.CONFIG = config
        self.fill_abs_path()

    
    def fill_abs_path(self):
        config = {}
        for k, v in self.CONFIG.items():
            if k.endswith('dir') or k.endswith('path'):
                new_path = os.path.join(util.ROOT, v)
                config[k] = new_path
                if k.endswith('dir') and not os.path.exists(new_path):
                    os.makedirs(new_path)
            else:
                config[k] = v
        self.CONFIG = config
        return None

    def run_map_doc_id(self):
        config = self.CONFIG
        webpages_dir = config['webpages_dir']
        mapped_webpages_dir = config['mapped_webpages_dir']
        id_mapper_pickle_dir = config['id_mapper_pickle_dir']
        print 'begin run map_doc_id'
        print 'save to %s' % id_mapper_pickle_dir
        map_doc_id.run(webpages_dir, mapped_webpages_dir, id_mapper_pickle_dir)
        print 'finish'
        return None

    def run_text_extraction(self):
        config = self.CONFIG
        webpages_dir = config['mapped_webpages_dir']
        body_text_dir = config['body_text_dir']
        log_path = config['log_path']
        print 'begin run text extraction from %s' % webpages_dir
        print 'save to %s' % body_text_dir
        text_extraction.run(webpages_dir, body_text_dir, log_path)
        print 'finish run text extraction to %s' % body_text_dir
        return None

    def run_feature_extractor(self):
        config = self.CONFIG
        body_text_dir = config['body_text_dir']
        feature_dir = config['feature_dir']
        print 'begin run feature extractor.'
        print 'Save features to %s' % feature_dir
        FeatureExtractor.run(body_text_dir, feature_dir)
        print 'finish save features to %s' % feature_dir
        return None

    def run_feature_filter(self):
        config = self.CONFIG
        feature_dir = config['feature_dir']
        selected_feature_dir = config['selected_feature_dir']
        print 'begin run feature filter.'
        print 'save selected features to %s' % selected_feature_dir
        feature_filter.run(feature_dir, selected_feature_dir)
        print 'finish save selected features to %s' % selected_feature_dir
        return None

    def run_feature_vector(self):
        config = self.CONFIG
        selected_feature_dir = config['selected_feature_dir']
        matrix_dir = config['matrix_dir']
        print 'begin run feature vector from %s' % selected_feature_dir
        print 'save matrix to %s' % matrix_dir
        feature_vector.run(selected_feature_dir, matrix_dir)
        print 'finish save matrix to %s' % matrix_dir
        return None

    def run_svd(self):
        config = self.CONFIG
        matrix_dir = config['matrix_dir']
        svd_matrix_dir = config['svd_matrix_dir']
        print 'begin run SVD from %s' % matrix_dir
        print 'save svd matrix to %s' % svd_matrix_dir
        svd.run(matrix_dir, svd_matrix_dir)
        print 'finish save svd matrix to %s' % svd_matrix_dir
        return None

    def run_consine(self, svd=True):
        config = self.CONFIG
        if svd:
            matrix_dir = config['svd_matrix_dir']
        else:
            matrix_dir = config['matrix_dir']
        cosine_dir = config['cosine_dir']
        print 'begin compute cosine similarity from %s' % matrix_dir
        print 'save to %s' % cosine_dir
        cosine_similarity.run(matrix_dir, cosine_dir)
        print 'finish save cosine similarity to %s' % cosine_dir
        return None

    def run_louvain(self):
        config = self.CONFIG
        cosine_dir = config['cosine_dir']
        louvain_category_dir = config['louvain_category_dir']
        print 'begin run louvain method from %s' % cosine_dir
        print 'save to %s' % louvain_category_dir
        louvain.run(cosine_dir, louvain_category_dir)
        print 'finish save louvain category to %s' % louvain_category_dir
        return None

    def run_gen_result(self):
        config = self.CONFIG
        category_dir = config['category_dir']
        before_map_back_result_dir = config['before_map_back_result_dir']
        print 'begin generating results from %s' % category_dir
        print 'save to %s' % before_map_back_result_dir
        gen_result.run(category_dir, before_map_back_result_dir)
        print 'finish save results to %s' % before_map_back_result_dir
        return None

    def run_map_back(self):
        config = self.CONFIG
        inverted_mapper_dir = config['id_mapper_pickle_dir']
        before_map_back_result_dir = config['before_map_back_result_dir']
        result_dir = config['result_dir']
        print 'begin map back from %s' % before_map_back_result_dir
        print 'save to %s' % result_dir
        map_back.run(inverted_mapper_dir, before_map_back_result_dir, result_dir)
        print 'finish save results to %s' % result_dir
        return None

    def run(self, step=1):
        processes_dict = {
            1: self.run_map_doc_id,
            2: self.run_text_extraction,
            3: self.run_feature_extractor,
            4: self.run_feature_filter,
            5: self.run_feature_vector,
            6: self.run_svd,
            7: self.run_consine,
            8: self.run_louvain,
            9: self.run_gen_result,
            10: self.run_map_back
        }
        processes = sorted(processes_dict.items())
        for no, func in processes:
            if step <= no:
                func()
        return None


def parse_cmd_args():
    parser = argparse.ArgumentParser(description='Execute a people clustering task')
    parser.add_argument('configure', help='The config path')
    parser.add_argument('-s', '--step', type=int, default=1, help='The process step to begin')
    args = parser.parse_args()
    config_path = os.path.abspath(args.configure)
    return config_path


def main():
    config_path = parse_cmd_args()
    with open(config_path) as cf:
        config = json.load(cf)
    t = Task(config)
    t.run()


if __name__ == '__main__':
    main()
