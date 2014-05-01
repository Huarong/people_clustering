#coding:utf-8

import os
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
        self.__init_tools()
        self.stops = []
        self.stopword_path = os.path.join(util.ROOT, 'dict/stopword.txt')
        self.load_stops()

    def __init_tools(self):
        test = "Just a test not for printing out or other use "
        tagger(tokenizer(test))
        segmenter(test)
        test = wn.synsets('test')

    def load_stops(self):
        with open(self.stopword_path) as f:
            stopSet = set([line.strip() for line in f.readlines()])
            self.stops.extend(list(stopSet))

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


    def extract(self, text, limit=1,tagList=['NN','VB','VBD']):
        sents = segmenter(text)
        tokens = []
        wordcount = 0
        for sent in sents:
            tokens.extend(tokenizer(sent))
        tagTube = tagger(tokens)

        wordDict = {}
        for term in tagTube:
            wordcount += 1
            if term[1] in tagList and term[0] not in self.stops:
                meanList = self.abstract(term[0],term[1],limit)
                for w in meanList:
                    wordDict[w] = wordDict.get(w,0) + 1

        return wordDict,wordcount


class TestFilter(unittest.TestCase):
    def test_filt(self):
        flt = FeatureExtractor()
        text = """This is a book about computer. If you like this book, I would give it to you.
        Do you like this book?
        """
        target = {'computer.n.01': 1, 'book.n.01': 3, 'give.v.01': 1}
        wordDict, count = flt.extract(text,1)
        print count
        self.assertDictEqual(target, wordDict)
        # print filt(text)

        # self.assertEqual("abcd", "abcf")


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
                features[rank] = flt.extract(text)
        features_pickle_path = os.path.join(feature_dir, '%s.json' % name)
        with open(features_pickle_path, 'wb') as fp:
            json.dump(features, fp)
        c += 1
        if(c==3):
            break
    return None


def main():
    body_text_dir = os.path.join(util.ROOT, 'pickle/2008train/bodytext/')
    feature_dir = os.path.join(util.ROOT, 'pickle/2008train/features/')
    run(body_text_dir, feature_dir)
    return None


if __name__ =="__main__":
    # unittest.main()
    main()
