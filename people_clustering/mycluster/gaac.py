#coding:utf-8

import copy

try:
    import numpy
except ImportError:
    pass

from util import VectorSpaceClusterer, Dendrogram, cosine_distance,euclidean_distance

class GAAClusterer(VectorSpaceClusterer):
    """
    The Group Average Agglomerative starts with each of the N vectors as singleton
    clusters. It then iteratively merges pairs of clusters which have the
    closest centroids.  This continues until there is only one cluster. The
    order of merges gives rise to a dendrogram: a tree with the earlier merges
    lower than later merges. The membership of a given number of clusters c, 1
    <= c <= N, can be found by cutting the dendrogram at depth c.

    This clusterer uses the cosine similarity metric only, which allows for
    efficient speed-up in the clustering process.
    """

    def __init__(self, num_clusters=1, normalise=True, svd_dimensions=None):
        VectorSpaceClusterer.__init__(self, normalise, svd_dimensions)
        self._num_clusters = num_clusters
        self._dendrogram = None
        self._groups_values = None
        self._distMap ={}

    def cluster(self, vectors, assign_clusters=False, DisType='cos',Stype='avg',trace=False):
        # stores the merge order
        l = len(vectors)
        if('cos'==DisType):
            for i in range(l):
                for j in range(i+1,l):
                    self._distMap[(i,j)] = cosine_distance(vectors[i], vectors[j])
        elif('euc'==DisType):
            for i in range(l):
                for j in range(i+1,l):
                    self._distMap[(i,j)] = euclidean_distance(vectors[i], vectors[j])
        self._dendrogram = Dendrogram(
            [numpy.array(vector, numpy.float64) for vector in vectors])
        result = VectorSpaceClusterer.cluster(self, vectors, assign_clusters, Stype, trace)
        print result
        return result

    def cluster_vectorspace(self, vectors, Stype, trace=False):
        # create a cluster for each vector
        l = len(vectors)
        clusters = [[i] for i in range(l)]

        # the sum vectors
        vector_sum = copy.copy(vectors)                 # 元素为 numpy.array()

        ADs = []
        results = []                        # 记录自底向上每层分类的结果
        while len(clusters) > max(self._num_clusters, 1):
            # find the two best candidate clusters to merge, based on their
            # S(union c_i, c_j)
            best = None
            dis = None
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    if ('avg'==Stype):
                        dis = self._average_similarity(
                                    vector_sum[i], len(clusters[i]),
                                    vector_sum[j], len(clusters[j]))
                    elif ('mean'==Stype):
                        dis = self._mean_similarity(clusters[i],clusters[j])
                    elif ('max'==Stype):
                        dis = self._max_similarity(clusters[i],clusters[j])
                    elif ('min'==Stype):
                        dis = self._min_similarity(clusters[i],clusters[j])

                    if not best or dis < best[0]:
                        best = (dis, i, j)

            # merge them and replace in cluster list
            i, j = best[1:]
            sum = clusters[i] + clusters[j]                  # list 直接相加
            if trace: print 'merging %d and %d' % (i, j)

            clusters[i] = sum
            del clusters[j]
            vector_sum[i] = vector_sum[i] + vector_sum[j]    # 元素为 numpy.array() , 对应位置累加
            del vector_sum[j]

            self._dendrogram.merge(i, j)
            print clusters

            AD = self._All_Dis(clusters)
            print AD
            ADs.append(AD)

            result = []
            for i in range(l):
                for j,c in enumerate(clusters):
                    if i in c:
                        result.append(j)
            print result
            print "*"*10
            results.append(result)

        l_ADs = len(ADs)
        minAD = ADs[0]
        min_index = 0
        for i in range(l_ADs):
            if (minAD>ADs[i]):
                min_index = i
                minAD = ADs[i]

        self.update_clusters(self._num_clusters)
        return results[min_index]

    def update_clusters(self, num_clusters):
        clusters = self._dendrogram.groups(num_clusters)
        print clusters
        self._centroids = []
        for cluster in clusters:
            assert len(cluster) > 0
            if self._should_normalise:
                centroid = self._normalise(cluster[0])
            else:
                centroid = numpy.array(cluster[0])
            for vector in cluster[1:]:
                if self._should_normalise:
                    centroid += self._normalise(vector)
                else:
                    centroid += vector
            centroid /= float(len(cluster))
            self._centroids.append(centroid)
        self._num_clusters = len(self._centroids)

    def classify_vectorspace(self, vector):
        best = None
        for i in range(self._num_clusters):
            centroid = self._centroids[i]
            sim = self._average_similarity(vector, 1, centroid, 1)
            if not best or sim > best[0]:
                best = (sim, i)
        return best[1]

    def dendrogram(self):
        """
        :return: The dendrogram representing the current clustering
        :rtype:  Dendrogram
        """
        return self._dendrogram

    def num_clusters(self):
        return self._num_clusters

    #///////////////////////// Similarity between two clusters ////////////////////////
    def _average_similarity(self, v1, l1, v2, l2):      # 两个 cluster 的平均相似性
        sum = v1 + v2
        length = l1 + l2
        return 1-(numpy.dot(sum, sum) - length) / (length * (length - 1))

    def _min_similarity(self,c1,c2):
        best = None
        for i in c1:
            for j in c2:
                dis = None
                if(i<j):
                    dis = self._distMap[(i,j)]
                else:
                    dis = self._distMap[(j,i)]
                if None==best or best > dis:
                    best = dis
        return best

    def _max_similarity(self,c1,c2):
        best = None
        for i in c1:
            for j in c2:
                dis = None
                if(i<j):
                    dis = self._distMap[(i,j)]
                else:
                    dis = self._distMap[(j,i)]
                if None==best or best < dis:
                    best = dis
        return best

    def _mean_similarity(self,c1,c2):
        sumD = 0
        count = 0
        for i in c1:
            for j in c2:
                count += 1
                dis = None
                if(i<j):
                    dis = self._distMap[(i,j)]
                else:
                    dis = self._distMap[(j,i)]
                sumD += dis
        mean = sumD/count
        return mean



    #///////////////////////////////////////////////////////////////////////////
    #/////////////////// 自定义每层 AD 值，用于确定要返回聚类层 /////////////////////
    def _All_Dis(self,clusters):
        l = len(clusters)
        Inter = 0
        Inner = 0

        #///////////////// distance sum between all ci and cj ////////////////
        for i in range(l):
            for j in range(i+1,l):
                for x in clusters[i]:
                    Inter += self._mean_similarity(clusters[i],clusters[j])

        #/////// distance sum between between every tow points in a class ////
        for i in range(l):
            size = len(clusters[i])
            for n in range(size):
                for m in range(n+1,size):
                    x = clusters[i][n]
                    y = clusters[i][m]
                    if(x>y):
                        Inner += self._distMap[(y,x)]
                    elif(x<y):
                        Inner += self._distMap[(x,y)]      
        print "Inner:",Inner,"Inter:",Inter
        return (Inner+Inter)*l
    #//////////////////////////////////////////////////////////////////////////////////

    def __repr__(self):
        return '<GroupAverageAgglomerative Clusterer n=%d>' % self._num_clusters


    #///////////////// 根据二维的样本点，和聚类结果，绘出结果散点图 /////////////////////////
    def draw_2D(self,vectors, result):
        import pylab as pl
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

        types = ['or','og','ob','oy','oc','ok','om','ow','^r','^g','^b','^y','^c','^k','^m','^w']
        for i in range(l):
            pl.plot(Xs[i],Ys[i],types[i])
        pl.xlim(-1,maxX+1)
        pl.ylim(-1,maxY+1)
        pl.show()
    #/////////////////////////////////////////////////////////////////////////////




#/////////////////////////////////////////////////////////////////////////////////
'''                                 测试部分                                    '''
#/////////////////////////////////////////////////////////////////////////////////
'''   半随机生成 n 个二维点样本， 大致属于 m 个类  '''
def rand_2D_vector(n,m):

    import random
    ms = numpy.sqrt(2*m)
    if(ms>int(ms)):     # 向上取整
        ms = int(ms) + 1
    else:
        ms = int(ms)

    tmp = []
    count = 0
    c = n/(2*ms)
    w = n/ms
    for i in range(ms):
        for j in range(ms):
            if((i%2)==(j%2)):
                pi0 = i*w
                pj0 = j*w
                pi1 = (i+1)*w
                pj1 = (j+1)*w
                for k in range(c):
                    x = random.randint(pi0, pi1)
                    y = random.randint(pj0, pj1)
                    tu = (x,y)
                    if(tu not in tmp):
                        tmp.append(tu)
                        count += 1
                        if(n==count):
                            break
    return tmp



'''    实例： 生成 250 个一个随机二维样本，大致属于 8 个类    '''
def demo():

    tmpV = rand_2D_vector(250,8)

    vectors = [numpy.array(f) for f in tmpV]

    clusterer = GAAClusterer(1)                 # 限定最少类的个数
    result = clusterer.cluster(vectors, False,"euc", "mean")    # 返回聚类结果列表

    clusterer.draw_2D(vectors, result)          # 绘制分类后的二维图


if __name__ == '__main__':
    demo()
