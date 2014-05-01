#coding:utf-8
# Natural Language Toolkit: Clusterer Utilities
#
# Copyright (C) 2001-2012 NLTK Project
# Author: Trevor Cohn <tacohn@cs.mu.oz.au>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT

import copy
from sys import stdout
from math import sqrt

try:
    import numpy 
except ImportError:
    pass

from api import ClusterI

class VectorSpaceClusterer(ClusterI):
    """
    Abstract clusterer which takes tokens and maps them into a vector space.
    Optionally performs singular value decomposition to reduce the
    dimensionality.
    """
    def __init__(self, normalise=False, svd_dimensions=None):
        """
        :param normalise:       should vectors be normalised to length 1
        :type normalise:        boolean
        :param svd_dimensions:  number of dimensions to use in reducing vector
                                dimensionsionality with SVD
        :type svd_dimensions:   int
        """
        self._Tt = None
        self._should_normalise = normalise
        self._svd_dimensions = svd_dimensions

    def cluster(self, vectors, assign_clusters=False, ClusterNum=None, Stype='avg', trace=False):
        assert len(vectors) > 0

        # normalise the vectors
        if self._should_normalise:
            vectors = map(self._normalise, vectors)

        # print vectors

        # use SVD to reduce the dimensionality
        if self._svd_dimensions and self._svd_dimensions < len(vectors[0]):
            [u, d, vt] = numpy.linalg.svd(numpy.transpose(numpy.array(vectors)))    # h × w -> w × h
            S = d[:self._svd_dimensions] * \
                numpy.identity(self._svd_dimensions, numpy.float64)     # d × d     # 对角为 1 的单位矩阵
            T = u[:,:self._svd_dimensions]                              # w × d
            Dt = vt[:self._svd_dimensions,:]                            # d × h
            vectors = numpy.transpose(numpy.dot(S, Dt))         # d × h --> h × d     
            self._Tt = numpy.transpose(T)                       # w × d --> d × w     

        # call abstract method to cluster the vectors
        result = self.cluster_vectorspace(vectors, ClusterNum,Stype, trace)                # h × d

        # assign the vectors to clusters
        if assign_clusters:
            # print "Tt:",self._Tt,"h × d", vectors
            return [self.classify(vector) for vector in vectors]
        else:
            return result

    def cluster_vectorspace(self, vectors, Stype, trace):
        """
        Finds the clusters using the given set of vectors.
        """
        raise NotImplementedError()

    def classify(self, vector):
        if self._should_normalise:
            vector = self._normalise(vector)
        if self._Tt is not None:
            vector = numpy.dot(self._Tt, vector)
        cluster = self.classify_vectorspace(vector)     # 返回类的 index
        return self.cluster_name(cluster)

    def classify_vectorspace(self, vector):
        """
        Returns the index of the appropriate cluster for the vector.
        """
        raise NotImplementedError()

    def likelihood(self, vector, label):
        if self._should_normalise:
            vector = self._normalise(vector)
        if self._Tt is not None:
            vector = numpy.dot(self._Tt, vector)
        return self.likelihood_vectorspace(vector, label)

    def likelihood_vectorspace(self, vector, cluster):
        """
        Returns the likelihood of the vector belonging to the cluster.
        """
        predicted = self.classify_vectorspace(vector)
        if cluster == predicted: return 1.0
        else:                    return 0.0

    def vector(self, vector):
        """
        Returns the vector after normalisation and dimensionality reduction
        """
        if self._should_normalise:
            vector = self._normalise(vector)
        if self._Tt is not None:
            vector = numpy.dot(self._Tt, vector)
        return vector

    def _normalise(self, vector):
        """
        Normalises the vector to unit length.
        """
        return vector / sqrt(numpy.dot(vector, vector))


#/////////////////////////////////// 共用函数 /////////////////////////////////////////////
def euclidean_distance(u, v):
    """
    Returns the euclidean distance between vectors u and v. This is equivalent
    to the length of the vector (u - v).
    """
    diff = u - v
    return sqrt(numpy.dot(diff, diff))

def cosine_distance(u, v):      # cos():为相似性， 1-cos():为相似性距离
    """
    Returns 1 minus the cosine of the angle between vectors v and u. This is equal to
    1 - (u.v / |u||v|).
    """
    su = sum(u)
    sv = sum(v)
    if (0==su and 0==sv):
        return 0
    elif (0==su or 0==sv):
        return 1
    else:
        return 1 - (numpy.dot(u, v) / (sqrt(numpy.dot(u, u)) * sqrt(numpy.dot(v, v))))

def load_matrix(path):
    matrix = []
    with open(path) as f:
        for line in f.readlines():
            row = [float(e) for e in line.split()]
            matrix.append(row)
    return matrix

def min_Angle_part(Dlist):
    l = len(Dlist)

    #-------------------- 分段表示样本平均曲线: Smooth1 ---------------------------
    c = float(l)/10
    if (c<1):
        c = 1
    elif (c > l/10):
        c = (l/10) + 1

    tmp = []
    count = 0
    while count < l:
        ccount = 0
        tmpv = 0
        while ccount < c and count < l:
            tmpv += Dlist[count]
            ccount += 1
            count +=1
        if (0!=ccount):
           tmp.append(float(tmpv)/ccount)
    #----------------------- 分段表示曲线再平滑：Smooth2 ----------------------
    ltmp = len(tmp)
    # Smoothtimes = 1
    # for i in range(Smoothtimes):
    #     for i in range(1,ltmp-1):
    #         tmp[i] = (Ttmp[i-1] + Ttmp[i] + Ttmp[i+1])/3
    #     Ttmp = copy.copy(tmp)
    
    angles = []
    angles.append(0.)
    for i in range(1,ltmp-1):
        l0 = numpy.sqrt((tmp[i+1]-tmp[i-1])*(tmp[i+1]-tmp[i-1])+4)
        l1 = numpy.sqrt((tmp[i]-tmp[i-1])*(tmp[i]-tmp[i-1])+1)
        l2 = numpy.sqrt((tmp[i+1]-tmp[i])*(tmp[i+1]-tmp[i])+1)
        angles.append(l1+l2-l0)
    angles.append(0.)

    minIndex = (ltmp/2)-1
    minAngle = angles[minIndex]
    for i in range(ltmp/2,ltmp):
        if (minAngle<angles[i]):
            minAngle = angles[i]
            minIndex = i
    part = ltmp - 1 - minIndex

    return tmp, angles, part  

def min_Angle_All(Dlist):
    tmp = copy.copy(Dlist)  # 不能破坏原始数据
    #----------------------- 分段表示曲线再平滑：Smooth2 ----------------------
    ltmp = len(tmp)
    # Smoothtimes = 1
    # for i in range(Smoothtimes):
    #     for i in range(1,ltmp-1):
    #         tmp[i] = (Ttmp[i-1] + Ttmp[i] + Ttmp[i+1])/3
    #     Ttmp = copy.copy(tmp)
    
    angles = []
    angles.append(0.)
    for i in range(1,ltmp-1):
        l0 = numpy.sqrt((tmp[i+1]-tmp[i-1])*(tmp[i+1]-tmp[i-1])+4)
        l1 = numpy.sqrt((tmp[i]-tmp[i-1])*(tmp[i]-tmp[i-1])+1)
        l2 = numpy.sqrt((tmp[i+1]-tmp[i])*(tmp[i+1]-tmp[i])+1)
        angles.append(l1+l2-l0)
    angles.append(0.)

    minIndex = (ltmp/2)-1
    minAngle = angles[minIndex]
    for i in range(ltmp/2,ltmp):
        if (minAngle<angles[i]):
            minAngle = angles[i]
            minIndex = i
    min_point = ltmp - 1 - minIndex

    return min_point


#///////////////// 根据二维的样本点，和聚类结果，绘出结果散点图 /////////////////////////
def draw_2D_cluster(vectors, result):
    if (2!=len(vectors[0])):
        return
    import matplotlib.pyplot as pl
    fig = pl.figure(figsize=(9,9))
    ax = fig.add_subplot(111)

    rList =list(set(result)) 
    l = len(rList)
    Xs = []
    Ys = []
    for i in range(l):
        Xs.append([])
        Ys.append([])

    maxX = 0
    maxY = 0
    for i,vector in enumerate(vectors):
        index = rList.index(result[i])
        Xs[index].append(vector[0])
        if (vector[0]>maxX):
            maxX = vector[0]
        Ys[index].append(vector[1])
        if (vector[1]>maxY):
            maxY = vector[1]

    types = ['or','og','ob','oy','oc','ok','om','ow','^r','^g','^b','^y','^c','^k','^m','^w',\
        '>r','>g','>b','>y','>c','>k','>m','>w','<r','<g','<b','<y','<c','<k','<m','<w',\
        'vr','vg','vb','vy','vc','vk','vm','vw','1r','1g','1b','1y','1c','1k','1m','1w',\
        '2r','2g','2b','2y','2c','2k','2m','2w','3r','3g','3b','3y','3c','3k','3m','3w',\
        'xr','xg','xb','xy','xc','xk','xm','xw','sr','sg','sb','sy','sc','sk','sm','sw',\
        '*r','*g','*b','*y','*c','*k','*m','*w','dr','dg','db','dy','dc','dk','dm','dw',\
        '+r','+g','+b','+y','+c','+k','+m','+w','hr','hg','hb','hy','hc','hk','hm','hw',\
        ]
    for i in range(l):
        ax.plot(Xs[i],Ys[i],types[i])
    pl.xlim(-1,maxX+1)
    pl.ylim(-1,maxY+1)
    pl.show()
#/////////////////////////////////////////////////////////////////////////////

def draw_2D_noise(realPTs,noisePTs):
    import matplotlib.pyplot as pl
    fig = pl.figure(figsize=(9,9))
    ax = fig.add_subplot(111)
    ax.plot([x[0] for x in realPTs],[y[1] for y in realPTs],'or')
    ax.plot([x[0] for x in noisePTs],[y[1] for y in noisePTs],'xr')
    pl.show()
#/////////////////////////////////////////////////////////////////////////////


#/////////////////// 根据一维数组作为 Y 值绘制变化曲线 /////////////////////////////
def draw_line(Ys):
    import matplotlib.pyplot as pl
    fig = pl.figure(figsize=(9,9))
    ax = fig.add_subplot(111)

    c = sorted(Ys)
    L = c[0]
    H = c[-1]
    ax.plot(Ys)
    pl.xlim(0,len(Ys)+1)
    pl.ylim(L,H)
    pl.show()

#///////////////////////////////////// Dendrogram /////////////////////////////////////////
class _DendrogramNode(object):
    """ Tree node of a dendrogram. """

    def __init__(self, value, *children):
        self._value = value
        self._children = children

    def leaves(self, values=True):
        if self._children:
            leaves = []
            for child in self._children:
                leaves.extend(child.leaves(values))
            return leaves
        elif values:
            return [self._value]
        else:
            return [self]

    def groups(self, n):
        queue = [(self._value, self)]

        while len(queue) < n:
            priority, node = queue.pop()
            if not node._children:
                queue.push((priority, node))
                break
            for child in node._children:
                if child._children:
                    queue.append((child._value, child))
                else:
                    queue.append((0, child))
            # makes the earliest merges at the start, latest at the end
            queue.sort()

        groups = []
        for priority, node in queue:
            groups.append(node.leaves())
        return groups

class Dendrogram(object):
    """
    Represents a dendrogram, a tree with a specified branching order.  This
    must be initialised with the leaf items, then iteratively call merge for
    each branch. This class constructs a tree representing the order of calls
    to the merge function.
    """

    def __init__(self, items=[]):
        """
        :param  items: the items at the leaves of the dendrogram
        :type   items: sequence of (any)
        """
        self._items = [_DendrogramNode(item) for item in items]
        self._original_items = copy.copy(self._items)
        self._merge = 1

    def merge(self, *indices):
        """
        Merges nodes at given indices in the dendrogram. The nodes will be
        combined which then replaces the first node specified. All other nodes
        involved in the merge will be removed.

        :param  indices: indices of the items to merge (at least two)
        :type   indices: seq of int
        """
        assert len(indices) >= 2
        node = _DendrogramNode(self._merge, *[self._items[i] for i in indices])
        self._merge += 1
        self._items[indices[0]] = node
        for i in indices[1:]:
            del self._items[i]

    def groups(self, n):
        """
        Finds the n-groups of items (leaves) reachable from a cut at depth n.
        :param  n: number of groups
        :type   n: int
        """
        if len(self._items) > 1:
            root = _DendrogramNode(self._merge, *self._items)
        else:
            root = self._items[0]
        return root.groups(n)

    def show(self, leaf_labels=[]):
        """
        Print the dendrogram in ASCII art to standard out.
        :param leaf_labels: an optional list of strings to use for labeling the leaves
        :type leaf_labels: list
        """

        # ASCII rendering characters
        JOIN, HLINK, VLINK = '+', '-', '|'

        # find the root (or create one)
        if len(self._items) > 1:
            root = _DendrogramNode(self._merge, *self._items)
        else:
            root = self._items[0]
        leaves = self._original_items

        if leaf_labels:
            last_row = leaf_labels
        else:
            last_row = [str(leaf._value) for leaf in leaves]

        # find the bottom row and the best cell width
        width = max(map(len, last_row)) + 1
        lhalf = width / 2
        rhalf = width - lhalf - 1

        # display functions
        def format(centre, left=' ', right=' '):
            return '%s%s%s' % (lhalf*left, centre, right*rhalf)
        def display(str):
            stdout.write(str)

        # for each merge, top down
        queue = [(root._value, root)]
        verticals = [ format(' ') for leaf in leaves ]
        while queue:
            priority, node = queue.pop()
            child_left_leaf = map(lambda c: c.leaves(False)[0], node._children)
            indices = map(leaves.index, child_left_leaf)
            if child_left_leaf:
                min_idx = min(indices)
                max_idx = max(indices)
            for i in range(len(leaves)):
                if leaves[i] in child_left_leaf:
                    if i == min_idx:    display(format(JOIN, ' ', HLINK))
                    elif i == max_idx:  display(format(JOIN, HLINK, ' '))
                    else:               display(format(JOIN, HLINK, HLINK))
                    verticals[i] = format(VLINK)
                elif min_idx <= i <= max_idx:
                    display(format(HLINK, HLINK, HLINK))
                else:
                    display(verticals[i])
            display('\n')
            for child in node._children:
                if child._children:
                    queue.append((child._value, child))
            queue.sort()

            for vertical in verticals:
                display(vertical)
            display('\n')

        # finally, display the last line
        display(''.join(item.center(width) for item in last_row))
        display('\n')

    def __repr__(self):
        if len(self._items) > 1:
            root = _DendrogramNode(self._merge, *self._items)
        else:
            root = self._items[0]
        leaves = root.leaves(False)
        return '<Dendrogram with %d leaves>' % len(leaves)


