from math import sqrt
from random import randint


class Cluster(object):
    def __init__(self):
        # 簇的所有特征向量
        self._fcs = []
        # 簇的中心点
        self._center = None

    def set_center(self, new_center):
        """
        设置中心点
        :param new_center: 新的中心点
        """
        self._center = new_center

    def get_center(self):
        return self._center

    def add_fc(self, fc):
        self._fcs.append(fc)

    def update_center(self):
        """
        更新中心点
        """
        # 特征向量中特征的数量
        feature_num = len(self._fcs[0])
        # 特征向量的数量
        fc_num = len(self._fcs)
        for i in range(feature_num):
            # 计算当前特征在所有特征向量上的总和
            current_sum = 0
            for fc in self._fcs:
                current_sum += fc[i]
            # 将中心点对应特征的值，更新为均值
            self._center[i] = current_sum / fc_num

    def distance(self, fc):
        """
        计算中心点和特征向量之间的距离
        :param fc:
        :return:
        """
        length = len(fc)
        distance = 0
        for i in range(length):
            distance += (self._center[i] - fc[i]) ** 2
        return sqrt(distance)


class KMeans(object):
    def __init__(self, k):
        self._k = k
        self._clusters = [Cluster() for i in range(self._k)]

    def _select_k_indexes(self, total_num):
        """
        选择 k 个索引，选出来的索引用于从数据集中随机挑选 k 个簇的中心点
        :param total_num:
        :return:
        """
        k_indexes = []
        while len(k_indexes) < self._k:
            # 生成一个随机索引
            index = randint(0, total_num - 1)
            if index not in k_indexes:
                k_indexes.append(index)
        # 循环结束，k_indexes 中已经有了 k 个随机且不重复的索引
        return k_indexes

    def _init_clusters(self, data_set):
        """
        初始化 KMeans 的 k 个 c 簇
        :param data_set: 数据集
        :return:
        """
        k_indexes = self._select_k_indexes(self._k, len(data_set))
        for i in range(self._k):
            self._clusters[i].set_center(data_set[k_indexes[i]])

    def get_cluster(self):
        return self._clusters

    def train(self, data_set, iter_times):
        """
        训练
        :param data_set: 数据集
        :param iter_times: 迭代次数
        :return:
        """
        # 初始化所有的 k 个簇
        self._init_clusters(data_set)
        # 特征向量的个数
        fc_num = len(data_set)
        # 进行 iter_times 次迭代
        for i in range(iter_times):
            # 循环数据集中的数据
            for j in range(fc_num):
                # 当前特征向量
                current_fc = data_set[j]
                # 记当前特征向量的归属cluster的索引为0，最小距离为何第一个簇的距离
                cluster_index = 0
                min_dist = self._clusters[0].distance(current_fc)
                # 计算当前特征向量的所有簇的距离
                for k in range(1, self._k):
                    current_dist = self._clusters[k].distance(current_fc)
                    # 打擂台算法，求出最小距离
                    if current_dist < min_dist:
                        cluster_index = k
                        min_dist = current_dist
                # 所有 k 个距离计算完成之后把当前的特征向量加入到指定的簇中
                self._clusters[cluster_index].add_fc(current_fc)
            # 数据集中的所有数据都迭代完成之后，开始更新每个簇的中心点
            for cluster in self._clusters:
                cluster.update_center()
