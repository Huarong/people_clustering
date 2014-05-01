#coding:utf-8

import os
import re
import json
import unittest
from collections import defaultdict

from nltk import word_tokenize as tokenizer
from nltk import pos_tag as tagger
from nltk import sent_tokenize as segmenter
from nltk.corpus import wordnet as wn

import util

class FeatureExtractor(object):
    """Extract content words from text;
       Abstract word means;
    """
    def __init__(self):
        super(FeatureExtractor, self).__init__()
        # self.__init_tools()
        self.stops = set()
        self.stopword_path = os.path.join(util.ROOT, 'dict/stopword.txt')
        self.load_stops()
        self.tag_list = set(['NN', 'JJ', 'VB'])

    def __init_tools(self):
        test = "Just a test not for printing out or other use "
        tagger(tokenizer(test))
        segmenter(test)
        test = wn.synsets('test')

    def load_stops(self):
        with open(self.stopword_path) as f:
            self.stops = set([line.strip() for line in f])

    def tag_convert(self,tag):
        if('NN'==tag):
            return 'n'
        elif('VB'==tag or 'VBD'==tag):
            return 'v'
        elif('JJ'==tag):
            return 'a'
        else:
            print "Tag convert failed, you should add you tag in your tag_convert() function!"


    def abstract(self, word, tag, limit):
        '''
        获取指定单词，指定词性的不超过limit个同义词集的 name 的 list
        word:  要获取同义词的单词
        tag:   单词的元词性（nltk 标记词性 ）
        limit: 限制返回的同义词集名称个数
        '''
        meanList = []
        newTag = self.tag_convert(tag)
        SynList = wn.synsets(word,newTag)
        l = len(SynList)
        if (0==l):
            meanList.append(word)
        elif (1==l):
            meanList.append(SynList[0].name)
        elif (l <= limit and l >=1):
            for i in range(l):
                meanList.append(SynList[i].name)
        elif (l > limit):
            for i in range(limit):
                meanList.append(SynList[i].name)
        return meanList

    def is_name_in_text(self, name, text):
        name_list = name.lower().split('_')
        lower_text = text.lower()
        sents = segmenter(lower_text)
        word_set = set()
        for sent in sents:
            tokens = tokenizer(sent)
            for t in tokens:
                word_set.add(t)
        for e in name_list:
            if e in word_set:
                return True
        return False


    def extract(self, name, text, limit=1, is_wordnet=False):
        if not self.is_name_in_text(name, text):
            return {}, 0
        tagList = self.tag_list
        stopwords = self.stops
        wordDict = {}
        filterd_dict = {}
        sents = segmenter(text)
        wordcount = 0
        for sent in sents:
            tokens = tokenizer(sent)
            terms = tagger(tokens)
            for t in terms:
                wordcount += 1
                key = '.'.join(t)
                try:
                    wordDict[key] += 1
                except KeyError:
                    wordDict[key] = 1

        for term_s, count in wordDict.items():
            splited = term_s.split('.')
            pos = splited[-1]
            if pos[:2] in tagList:
                word = splited[0]
                if word not in stopwords:
                    if is_wordnet:
                        meanList = self.abstract(word, pos, limit)
                        for w in meanList:
                            filterd_dict[term_s] = count
                    else:
                        filterd_dict[term_s] = count

        return filterd_dict, wordcount


class TestFilter(unittest.TestCase):
    def test_filt(self):
        flt = FeatureExtractor()
        text = """This is a book about computer. If you like this book, I would give it to you.
        Do you like this book? It is a beautiful book.
        """
        # with wordnet
        # target = {'computer.n.01': 1, 'book.n.01': 4, 'beautiful.a.01': 1, 'give.v.01': 1}
        # without wordnet
        target = {'Do.NNP': 1, 'book.NN': 4, 'like.VBP': 1, 'give.VB': 1, 'beautiful.JJ': 1, 'computer.NN': 1}
        filtered_dict, count = flt.extract('book', text)
        print filtered_dict
        self.assertDictEqual(target, filtered_dict)

        text = """This is why we fought for health care reform. Read their stories.
        "You and I, as citizens, have the power to set this country's course."
        """
        target = {'set.VB': 1, 'Read.NNP': 1, 'fought.VBD': 1, 'course.NN': 1, 'citizens.NNS': 1, 'care.NN': 1, 'country.NN': 1, 'health.NN': 1, 'power.NN': 1, 'reform.NN': 1, 'stories.NNS': 1}
        filtered_dict, count = flt.extract('huo', text)
        print filtered_dict
        target = {}
        self.assertDictEqual(target, filtered_dict)


@util.timer
def run(body_text_dir, feature_dir):
    flt = FeatureExtractor()
    if not os.path.exists(feature_dir):
        os.makedirs(feature_dir)
    c = 0
    for name in os.listdir(body_text_dir):
        name_dir = os.path.join(body_text_dir, name)
        features = {}
        print 'begin %s' % name
        for rank_file_name in os.listdir(name_dir):
            rank = rank_file_name.split('.')[0]
            print 'start %s' % rank_file_name
            with open(os.path.join(name_dir, rank_file_name)) as rank_file:
                text = rank_file.read()
                features[rank] = flt.extract(name, text)
        features_pickle_path = os.path.join(feature_dir, '%s.json' % name)
        with open(features_pickle_path, 'wb') as fp:
            json.dump(features, fp)
        # c += 1
        # if(c==1):
        #     break
    return None


def main():
    body_text_dir = os.path.join(util.ROOT, 'pickle/2008train/bodytext/')
    feature_dir = os.path.join(util.ROOT, 'pickle/2008train/features/')
    run(body_text_dir, feature_dir)
    return None


if __name__ =="__main__":
    unittest.main()
    # main()
