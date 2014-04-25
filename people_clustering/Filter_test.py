#coding:utf-8

import unittest

from nltk import word_tokenize as tokenizer
from nltk import pos_tag as tagger
from nltk import sent_tokenize as segmenter
from nltk.corpus import wordnet as wn

class Filter(object):
    """Extract content words from text;
       Abstract word means;
    """
    def __init__(self):
        super(Filter, self).__init__()
        self.__init_tools()

    def __init_tools(self):
        test = "Just a test not for printing out or other use "
        tagger(tokenizer(test))
        segmenter(test)

    def filt(self, text, tagList=['NN','VB','VBD']):
        sents = segmenter(text)
        tokens = []
        for sent in sents:
            tokens.extend(tokenizer(sent))
        tagTube = tagger(tokens)

        wordDict = {}
        for term in tagTube:
            if term[1] in tagList:
                wordDict[term[0]] = wordDict.get(term[0],0) + 1

        return wordDict


class TestFilter(unittest.TestCase):
    def test_filt(self):
        flt = Filter()
        text = """This is a book about computer. If you like this book, I would give it to you.
        Do you like this book?
        """
        target = {'book': 3, 'computer': 1, 'give': 1}
        self.assertDictEqual(target, flt.filt(text))


if __name__ =="__main__":
    unittest.main()
