# scoding=utf-8

import pylab as pl
import numpy as np
from collections import defaultdict,Counter
from RandSample import rand_2D_vector_rect,rand_2D_vector_circle,real_matrix,noise_2D_vector_rect
from util import euclidean_distance,cosine_distance,min_Angle
from AD_Cluster import AD_Cluster



class DBCluster(object):   
    """
    DB_cluster  ： 实现基于密度的聚类
    EPs         ： 最小距离
    MinPts      ： 核心
    """  
    def __init__(self, Eps=None, MinPts = None):
        super(DBCluster, self).__init__()  
        self.Eps = Eps
        self.MinPts = MinPts
        self.distList = None

    def cluster(self, matrix):
        l = len(matrix)
        #---------------------------------------------------------------------------------------
        self.distList = np.zeros((l,l),np.float)
        for i in range(l):
            self.distList[i][i] = float('inf')      # 自身不参与聚类比较
            for j in range(i+1,l):
                self.distList[i][j] = euclidean_distance(np.array(matrix[i]), np.array(matrix[j]))
                self.distList[j][i] = self.distList[i][j]
        #----------------------------------------------------------------------------------------
        mostSimList = []        # 记录与第 i 个样本最相似的前 m 个样本的距离
        m = 3
        marks = [i for i in range(l)]

        for i in range(l):
            lis = self.distList[i].tolist()
            lis = zip(marks,lis)
            mostSimList.append(sorted(lis, key=lambda x:x[1])[0:m])

        ADist = []
        for i in range(l):
            ADist.append(mostSimList[i][m-1][1])
            ADist = sorted(ADist)

        mostSimList = zip(marks,mostSimList)
        mostSimList = sorted(mostSimList, key=lambda x:x[1][m-1][1], reverse=True)

        noise = []
        for i in mostSimList[0:l/5]:
            noise.append(i[0])

        #-----------------------------------------------------------------------------------------
        print mostSimList
        print ADist
        print noise
        return ADist , noise


def demo():
    points = noise_2D_vector_rect(500, 4)

    cluster2 = DBCluster()
    ADist, noise = cluster2.cluster(points)

    realPTs = []
    noisePTs = []
    for i, p in enumerate(points):
        if i in noise:
            noisePTs.append(p)
        else:
            realPTs.append(p)

    # cluster1 = AD_Cluster()
    # vectors0 = [np.array(f) for f in points]
    # vectors1 = [np.array(f) for f in realPTs]
    # cluster1.cluster(vectors0)


    pl.plot([x[0] for x in realPTs],[y[1] for y in realPTs],'or')
    pl.plot([x[0] for x in noisePTs],[y[1] for y in noisePTs],'ok')
    pl.show()
    pl.plot(ADist)
    pl.show()

    tmp,angles,part = denoise(ADist)
    print tmp,angles
    print part
    pl.plot(tmp)
    pl.show()
    pl.plot(angles)
    pl.show()

    # cluster1.cluster(vectors1)
    # 计算每个数据点相邻的数据点，邻域定义为以该点为中心以边长为2*EPs的网格

    matrix = real_matrix()  

if __name__=="__main__":
    demo()
        
# Eps = 3
# surroundPoints = defaultdict(list)
# for idx1,point1 in enumerate(points):
# 	for idx2,point2 in enumerate(points):
# 		if (idx1 < idx2):
# 			if(abs(point1[0]-point2[0])<=Eps and abs(point1[1]-point2[1])<=Eps):
# 				surroundPoints[idx1].append(idx2)
# 				surroundPoints[idx2].append(idx1)

# # 定义邻域内相邻的数据点的个数大于4的为核心点
# MinPts = 1
# corePointIdx = [pointIdx for pointIdx,surPointIdxs in surroundPoints.iteritems() if len(surPointIdxs)>=MinPts]

# # 邻域内包含某个核心点的非核心点，定义为边界点
# borderPointIdx = []
# for pointIdx,surPointIdxs in surroundPoints.iteritems():
# 	if (pointIdx not in corePointIdx):
# 		for onesurPointIdx in surPointIdxs:
# 			if onesurPointIdx in corePointIdx:
# 				borderPointIdx.append(pointIdx)
# 				break

# # 噪音点既不是边界点也不是核心点
# noisePointIdx = [pointIdx for pointIdx in range(len(points)) if pointIdx not in corePointIdx and pointIdx not in borderPointIdx]

# corePoint = [points[pointIdx] for pointIdx in corePointIdx]	
# borderPoint = [points[pointIdx] for pointIdx in borderPointIdx]
# noisePoint = [points[pointIdx] for pointIdx in noisePointIdx]

# # pl.plot([eachpoint[0] for eachpoint in corePoint], [eachpoint[1] for eachpoint in corePoint], 'or')
# # pl.plot([eachpoint[0] for eachpoint in borderPoint], [eachpoint[1] for eachpoint in borderPoint], 'oy')
# # pl.plot([eachpoint[0] for eachpoint in noisePoint], [eachpoint[1] for eachpoint in noisePoint], 'ok')

# groups = [idx for idx in range(len(points))]

# # 各个核心点与其邻域内的所有核心点放在同一个簇中
# for pointidx,surroundIdxs in surroundPoints.iteritems():
# 	for oneSurroundIdx in surroundIdxs:
# 		if (pointidx in corePointIdx and oneSurroundIdx in corePointIdx and pointidx < oneSurroundIdx):
# 			for idx in range(len(groups)):
# 				if groups[idx] == groups[oneSurroundIdx]:
# 					groups[idx] = groups[pointidx]

# # 边界点跟其邻域内的某个核心点放在同一个簇中
# for pointidx,surroundIdxs in surroundPoints.iteritems():
# 	for oneSurroundIdx in surroundIdxs:
# 		if (pointidx in borderPointIdx and oneSurroundIdx in corePointIdx):
# 			groups[pointidx] = groups[oneSurroundIdx]
# 			break

# # 取簇规模最大的5个簇
# wantGroupNum = 5
# finalGroup = Counter(groups).most_common(5)
# finalGroup = [onecount[0] for onecount in finalGroup]

# group1 = [points[idx] for idx in xrange(len(points)) if groups[idx]==finalGroup[0]]
# group2 = [points[idx] for idx in xrange(len(points)) if groups[idx]==finalGroup[1]]
# group3 = [points[idx] for idx in xrange(len(points)) if groups[idx]==finalGroup[2]]
# group4 = [points[idx] for idx in xrange(len(points)) if groups[idx]==finalGroup[3]]
# group5 = [points[idx] for idx in xrange(len(points)) if groups[idx]==finalGroup[4]]

# pl.plot([eachpoint[0] for eachpoint in group1], [eachpoint[1] for eachpoint in group1], 'or')
# pl.plot([eachpoint[0] for eachpoint in group2], [eachpoint[1] for eachpoint in group2], 'oy')
# pl.plot([eachpoint[0] for eachpoint in group3], [eachpoint[1] for eachpoint in group3], 'og')
# pl.plot([eachpoint[0] for eachpoint in group2], [eachpoint[1] for eachpoint in group4], 'ob')
# pl.plot([eachpoint[0] for eachpoint in group3], [eachpoint[1] for eachpoint in group5], 'ow')

# # 打印噪音点，黑色
# pl.plot([eachpoint[0] for eachpoint in noisePoint], [eachpoint[1] for eachpoint in noisePoint], 'ok')	

# pl.show()