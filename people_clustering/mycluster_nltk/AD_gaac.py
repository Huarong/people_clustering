#coding:utf-8

import copy

try:
    import numpy
except ImportError:
    pass

from util import VectorSpaceClusterer, Dendrogram, cosine_distance,euclidean_distance

class AD_Clusterer(VectorSpaceClusterer):
    """
    实现对无噪声、类数未知的样本进行精确聚类

    """

    def __init__(self, num_clusters=None, normalise=True, svd_dimensions=None):
        VectorSpaceClusterer.__init__(self, normalise, svd_dimensions)
        self._num_clusters = num_clusters
        self._groups_values = None
        self._distMap ={}

    def cluster(self, vectors, assign_clusters=False,ClusterNum=None, DisType='cos',Stype='avg',trace=False):
        # stores the merge order

        #-------------------------------------------------
        self._distMap.clear()   # 每次聚类不同样本之前必须更新
        #-------------------------------------------------

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
        result = VectorSpaceClusterer.cluster(self, vectors,assign_clusters,ClusterNum, Stype, trace)

        if(2==len(vectors[0])):         # 二维样本则显示可视化结果
            self.draw_2D(vectors, result)
            
        return result

    def cluster_vectorspace(self, vectors, ClusterNum, Stype, trace=False):
        l = len(vectors)
        #-----------------------------------------------------
        results = []        # 记录自底向上每层分类的结果
        ADs = []            # 记录每层的 AD 值
        #-----------------------------------------------------
        clusters = [[i] for i in range(l)]
        #----------------------- 初始化 -----------------------
        result = [(i,) for i in range(l)]
        AD = self._All_Dis(clusters)
        results.append(result)
        ADs.append(AD)
        #-----------------------------------------------------
        # the sum vectors
        vector_sum = copy.copy(vectors)                 # 元素为 numpy.array()
        while len(clusters) > 1:
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

            AD = self._All_Dis(clusters)
            ADs.append(AD)

            result = []
            for i in range(l):
                for j,c in enumerate(clusters):
                    if i in c:
                        result.append((j,))
            # print result
            # print "*"*10
            results.append(result)

        # if(1==self._num_clusters):
        #     ADs.append(0)
        #     results.append([(0,)])

        l_ADs = len(ADs)
        minAD = ADs[0]
        min_index = 0
        for i in range(l_ADs):
            if (minAD>ADs[i]):
                min_index = i
                minAD = ADs[i]
        if(None==ClusterNum):
            return results[min_index]
        elif(ClusterNum>l):
            print "The number of samples is less than the number of clusters specified! "
            print "The default result is return."
            return results[min_index]
        else:
            return results[l-ClusterNum]

        return results[min_index]

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
                    Inter += self._mean_similarity(clusters[i],clusters[j])#*(len(clusters[i])+len(clusters[j]))

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
        print "Cluster number = ",l    
        print "Inner:",Inner,"Inter:",Inter

        # if (1==l):          # 惩罚只分一类的情况，使其与不分类的效果一样
        #     l = len(clusters[0])
        AD = (Inner+Inter)*l
        print 'AD = ',AD
        # print "Clusters : ",clusters          # 太长，输出很慢
        print ""
        return AD
    #//////////////////////////////////////////////////////////////////////////////////

    def __repr__(self):
        return '<GroupAverageAgglomerative Clusterer n=%d>' % self._num_clusters


    #///////////////// 根据二维的样本点，和聚类结果，绘出结果散点图 /////////////////////////
    def draw_2D(self,vectors, result):
        import matplotlib.pyplot as pl
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
        'xr','xg','xb','xy','xc','xk','xm','xw','sr','sg','sb','sy','sc','sk','sm','sw']
        for i in range(l):
            pl.plot(Xs[i],Ys[i],types[i])
        pl.xlim(-1,maxX+1)
        pl.ylim(-1,maxY+1)
        pl.show()

    #/////////////////////////////////////////////////////////////////////////////




#/////////////////////////////////////////////////////////////////////////////////
'''                                 测试部分                                    '''
#/////////////////////////////////////////////////////////////////////////////////



'''    实例： (1) 生成 250 个半随机二维样本，大致属于 8 个类    
             (2) 生成 100 个半随机二维样本，大致属于 4 各类
'''
def demo():
    from RandSample import rand_2D_vector_circle, rand_2D_vector_rect

    tmpV1 = rand_2D_vector_rect(150,8)
    tmpV2 = rand_2D_vector_rect(200,8)

    # tmpV = [(5,6),(5,7),(6,6),(6,7)]

    tmpV3 = rand_2D_vector_circle(200,2)
    # result3 = []
    # for i in range(len(tmpV3)):
    #     result3.append(i)
    # # result3 =[0]*len(tmpV3)

    vectors1 = [numpy.array(f) for f in tmpV1]
    vectors2 = [numpy.array(f) for f in tmpV2]
    vectors3 = [numpy.array(f) for f in tmpV3]

    clusterer = AD_Clusterer(1)                 # 限定最少类的个数
    # result1 = clusterer.cluster(vectors1, False,None,"euc", "max")    # 返回聚类结果列表
    # result2 = clusterer.cluster(vectors2, False,None,"euc", "min")
    result3 = clusterer.cluster(vectors3, False,2,"euc", "min")
    # clusterer.draw_2D(vectors1, [i for i in result1])          # 绘制分类后的二维图
    # clusterer.draw_2D(vectors2, [i for i in result2]) 
    # clusterer.draw_2D(tmpV3, result3)

if __name__ == '__main__':
    demo()
