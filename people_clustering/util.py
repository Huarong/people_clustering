#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print ROOT


def init_log(logname, filename, level=logging.DEBUG, console=True):
    # make log file directory when not exist
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
 
    # set up logging to file - see previous section for more details
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename=filename,
                        filemode='a')
    # Now, define a couple of other loggers which might represent areas in your
    # application:
    logger = logging.getLogger(logname)
    if console:
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the the current logger
        logger.addHandler(console)
    return logger

def get_topicMatrix(Matrix, topicNum, fill = True):
    h,w = Matrix.shape
    if(True==fill):
        add = float(np.sum(Matrix))/(h*w)
        tmp = np.zeros((h,w), dtype=np.float32)
        for i in range(h):
            for j in range(w):
                if(0==Matrix[i][j]):
                    tmp[i][j] += add
                else:
                    tmp[i][j] += float(Matrix[i][j])
        Matrix = tmp
    m = min(h,w)
    if (m<topicNum):
        print "topicNum is large than the minor dimension of the Matrix!"
        sys.exist()
    u,s,v = np.linalg.svd(Matrix)
    l = len(s)
    sm = np.zeros((l,l))
    for i in range(topicNum):
        sm[i][i] = s[i]

    if(h<w):
        Matrix2 = (u.dot(sm)).dot(v[0:h,0:w])
    else:
        Matrix2 = (u[0:h,0:w].dot(sm)).dot(v)

    return Matrix2

def test_get_topicMatrix():
    n = np.array([[4, 3, 2, 1, 0],[0, 3, 2, 1, 0],[4, 4, 2, 7, 0],[1, 0, 0, 0, 0],[0, 0, 0, 1, 1]])
    tm = get_topicMatrix(n, 2,False)
    print tm


def timer(func, logger=None):
    def wrapper(*arg, **kw):
        t1 = time.time()
        func(*arg, **kw)
        t2 = time.time()
        infomation = '%0.4f sec %s' % ((t2-t1), func.func_code)
        if logger:
            logger.info(infomation)
        else:
            print infomation
        return None
    return wrapper


if __name__=="__main__":
	test_get_topicMatrix()