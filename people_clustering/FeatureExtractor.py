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
from nltk import FreqDist
from lxml import etree

import util


class FeatureExtractor(object):
    email_reg = re.compile(r'[a-zA-Z0-9_.+-]+@(?:[a-zA-Z0-9-]+)(?:\.[a-zA-Z0-9-]+)+')
    """Extract content words from text;
       Abstract word means;
    """
    def __init__(self, config):
        super(FeatureExtractor, self).__init__()
        # self.__init_tools()
        self.metadata_dir = config['metadata_dir']
        self.id_mapper_pickle_dir = config['id_mapper_pickle_dir']
        self.config = config
        self.stops = set()
        self.stopword_path = os.path.join(util.ROOT, 'dict/stopword.txt')
        self.load_stops()
        # self.tag_list = set(['NN', 'JJ', 'VB'])
        self.tag_list = set(['NN',])

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

    def is_name_in_text(self, name_list, text):
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


    def extract(self, name, name_list, text, limit=1, is_wordnet=False):
        if not self.is_name_in_text(name_list, text):
            return {}, 0
        tagList = self.tag_list
        stopwords = self.stops
        wordDict = {}
        filterd_dict = {}
        sents = segmenter(text)
        wordcount = 0
        for sent in sents:
            tokens = tokenizer(sent.lower())
            terms = tagger(tokens)
            for t in terms:
                wordcount += 1
                key = '.'.join(t)
                try:
                    wordDict[key] += 1
                except KeyError:
                    wordDict[key] = 1

        for term_s, count in wordDict.items():
            try:
                word, pos = term_s.split('.')
            except ValueError:
                continue
            if pos[:2] in tagList and word.lower() not in stopwords and len(word) >= 3:
                print word, pos
                if is_wordnet:
                    meanList = self.abstract(word, pos, limit)
                    for w in meanList:
                        filterd_dict[term_s] = count
                else:
                    filterd_dict[term_s] = count

        return filterd_dict, wordcount

    @staticmethod
    def clean_word(word):

        def is_alpha(c):
            return c.isalpha()

        return filter(is_alpha, word)

    def title_tokenize(self, title):
        title = title.lower()
        title_tokens = [self.clean_word(t) for t in tokenizer(title) if t not in self.stops and len(t) >= 3]
        title_tokens = [e for e in title_tokens if e]
        title_freq = dict(FreqDist(title_tokens))
        return title_freq

    def url_tokenize(self, url):
        url = url.lower()
        url_tokens = re.split('[/.]', url)
        url_tokens = [self.clean_word(t) for t in url_tokens if t and t not in set(['http:', 'https:', 'www', 'html', 'htm', 'shtml'])]
        url_tokens = [e for e in url_tokens if e]
        url_freq = dict(FreqDist(url_tokens))
        return url_freq

    def snippet_tokenize(self, snippet):
        snippet = snippet.lower()
        snippet_tokens = [self.clean_word(t) for t in tokenizer(snippet) if t not in self.stops and len(t) >=3 and t != '...']
        snippet_tokens = [e for e in snippet_tokens if e]
        snippet_freq = dict(FreqDist(snippet_tokens))
        return snippet_freq

    def email_detect(self, text):
        emails = self.email_reg.findall(text)
        email_freq = dict(FreqDist(emails))
        return email_freq

    def extra_extract(self, name, name_body_text):
        id_mapper_path = os.path.join(util.ROOT, self.id_mapper_pickle_dir, '%s.json' % name)
        id_mapper = util.load_pickle(id_mapper_path, typ='json')
        extra_features = {}
        metadata_path = os.path.join(self.metadata_dir, '%s.xml' % name)
        with open(metadata_path) as f:
            content = f.read()
        corpus = etree.XML(content)
        for doc in corpus:
            rank = doc.get('rank')
            mapped_rank = id_mapper[rank]
            # The description file opposite the snippet and title
            title = doc.xpath('./snippet')[0].xpath('string()')
            title_freq = self.title_tokenize(title)
            url = doc.get('url')
            url_freq = self.url_tokenize(url)
            snippet = doc.get('title')
            snippet_freq = self.snippet_tokenize(snippet)
            body_text_path = os.path.join(name_body_text, '%s.txt' % mapped_rank)
            with open(body_text_path) as f:
                email_freq = self.email_detect(f.read())
            extra_features[mapped_rank] = {'title': title_freq,
                                           'url': url_freq,
                                           'snippet': snippet_freq,
                                           'emails': email_freq}
        return extra_features


class TestFilter(unittest.TestCase):
    def setUp(self):
        config_path = util.abs_path('configure/2007test.NN.nltk.json')
        config = util.load_pickle(config_path, typ='json')
        self.flt = FeatureExtractor(config)

    def test_is_name_in_text(self):
        name_list = ['amanda', 'lentz']
        text = """1st World Cup Trampolin1999 1st World Cup Trampolin 1999/2000 1999 May, the 13th, in Aachen/GER TUMBLING M e n - W o m e n T umbling M E N W o m e n Rank N a m e Nation Prelimenary Finale 1 Rayshine Harris USA 54,79 29,89 2 Christopher Gigou FRA 52,06 28,06 3 Rasoslaw Walczak POL 51,40 27,83 4 Alexandre Dechanet FRA 52,82 27,80 4 Nicolas Fournials FRA 52,06 27,80 6 Adrian Sienkiewicz POL 50,69 27,70 7 Christian Celini BEL 50,26 26,93 8 Sergio Nascimento POR 50,66 26,06 9 Simon Rawlings GBR 49,52 26,03 10 Rune Kustensen DEN 49,92 25,60 11 Nicollas Divry FRA 49,89 12 Tomasz Kies POL 49,46 13 Martin Nielsen DEN 49,26 14 Randy Direen USA 48,73 15 Ihar Adamenkav BLR 48,26 16 Nuno Fernandes POR 47,82 17 Bartosz Dondajewski POL 46,72 18 Brian Hansen DEN 45,96 19 Eduardo Mendes POR 43,63 20 Robert Small GBR 40,99 T umbling L A D I E S M e n Rank N a m e Nation Prelimenary Final 1 Chrysel Robert FRA 49,26 26,46 2 Amanda Lentz USA 52,13 26,26 3 Melanie Thompson GBR 46,43 26,10 4 Peggy Pachy FRA 47,19 24,80 5 Mariana N Dour FRA 47,19 24,73 6 Wiktoria Weselak POL 47,66 24,33 7 Kathryn Peberdm GBR 48,69 22,23 8 Maryna Vashkevich BLR 43,16 21,13 9 Melanie Avisse FRA 43,46 10 Nikki Ahrens AUS 41,89 11 Kristy Wilson AUS 38,93 12 Lajcana Davis USA 36,56 TR men TRwomen SYN men SYNwom TUMmen TUMwomen back to G Y M home page G Y Mmedia-info-service /13-05-1999 - ehe -"""
        target = True
        get = self.flt.is_name_in_text(name_list, text)
        self.assertEqual(target, get)

        text = """This is why we fought for health care reform. Read their stories.
        "You and I, as citizens, have the power to set this country's course."
        """
        target = False
        get = self.flt.is_name_in_text(name_list, text)
        self.assertEqual(target, get)

    def test_filt(self):
        flt = self.flt
        text = """This is a book about computer. If you like this book, I would give it to you.
        Do you like this book? It is a beautiful book.
        """
        # with wordnet
        # target = {'computer.n.01': 1, 'book.n.01': 4, 'beautiful.a.01': 1, 'give.v.01': 1}
        # without wordnet
        target = {'Do.NNP': 1, 'book.NN': 4, 'like.VBP': 1, 'give.VB': 1, 'beautiful.JJ': 1, 'computer.NN': 1}
        filtered_dict, count = flt.extract('book', ['book'], text)
        print filtered_dict
        self.assertDictEqual(target, filtered_dict)

        text = """This is why we fought for health care reform. Read their stories.
        "You and I, as citizens, have the power to set this country's course."
        """
        target = {'set.VB': 1, 'Read.NNP': 1, 'fought.VBD': 1, 'course.NN': 1, 'citizens.NNS': 1, 'care.NN': 1, 'country.NN': 1, 'health.NN': 1, 'power.NN': 1, 'reform.NN': 1, 'stories.NNS': 1}
        filtered_dict, count = flt.extract('huo', ['huo'], text)
        print filtered_dict
        target = {}
        self.assertDictEqual(target, filtered_dict)

    def test_email_detect(self):
        text = 'My email looks like this: shcd+xsd@scd.com.cn. thank you. And yours is scdc.12@google.com.'
        target = ['shcd+xsd@scd.com.cn', 'scdc.12@google.com']
        get = self.flt.email_detect(text)
        self.assertListEqual(target, get)


@util.timer
def run(body_text_dir, feature_dir, config):
    flt = FeatureExtractor(config)
    util.makedir(feature_dir)
    c = 0
    for name in os.listdir(body_text_dir):
        name_dir = os.path.join(body_text_dir, name)
        features = {}
        print 'begin %s' % name
        name_list = name.lower().split('_')
        for rank_file_name in os.listdir(name_dir):
            rank = rank_file_name.split('.')[0]
            print 'start %s' % rank_file_name
            with open(os.path.join(name_dir, rank_file_name)) as rank_file:
                text = rank_file.read()
                features[rank] = flt.extract(name, name_list, text)
        features_pickle_path = os.path.join(feature_dir, '%s.json' % name)
        with open(features_pickle_path, 'wb') as fp:
            json.dump(features, fp)
        # c += 1
        # if(c==1):
        #     break
        break
    return None


@util.timer
def run_extra(body_text_dir, extra_feature_dir, config):
    flt = FeatureExtractor(config)
    util.makedir(extra_feature_dir)
    c = 0
    for name in os.listdir(body_text_dir):
        name_body_dir = os.path.join(body_text_dir, name)
        extra_features = {}
        print 'begin %s' % name
        extra_features = flt.extra_extract(name, name_body_dir)
        features_pickle_path = os.path.join(extra_feature_dir, '%s.json' % name)
        with open(features_pickle_path, 'wb') as fp:
            json.dump(extra_features, fp)
        # c += 1
        # if(c==1):
        #     break
    return None


def main():
    body_text_dir = os.path.join(util.ROOT, 'pickle/2008test/bodytext/')
    feature_dir = os.path.join(util.ROOT, 'pickle/2008test/features/')
    run(body_text_dir, feature_dir)
    return None


if __name__ =="__main__":
    unittest.main()
    # main()
