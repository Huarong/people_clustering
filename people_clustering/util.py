#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import pickle
import json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, ROOT)


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


def load_matrix(path):
    matrix = []
    with open(path) as f:
        for line in f.readlines():
            row = [float(e) for e in line.split()]
            matrix.append(row)
    return matrix


def dump_matrix(matrix, path):
    with open(path, 'wb') as out:
        for row in matrix:
            out.write(' '.join([str(e) for e in row]))
            out.write(os.linesep)
    print 'Finish writing matrix to %s' % path
    return None


def pickle_me(obj, path, typ=None):
    with open(path, 'wb') as f:
        if typ == 'json':
            json.dump(obj, f)
        else:
            pickle.dump(obj, f)
    return None


def load_pickle(path, typ=None):
    with open(path, 'wb') as f:
        if typ == 'json':
            return json.load(f)
        else:
            return pickle.load(f)


def makedir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return None


def abs_path(path):
    global ROOT
    return os.path.join(ROOT, path)
