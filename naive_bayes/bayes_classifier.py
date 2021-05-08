# encoding=utf-8

import numpy as np


class BayesClassifier(object):
    def __init__(self):
        self.prior_probability = np.load("../model/先验概率矩阵.npy")
        self.conditional_probability = np.load("../model/条件概率矩阵.npy")[:9]
        self.category_num = 9  # 其实也可以不要，因为是固定的；
        print(self.conditional_probability.shape)
        self.conditional_probability += 1  # 整个矩阵 + 1
        print(self.conditional_probability)
        all_news = self.prior_probability.reshape(9, 1)  # 将分类总数立起
        all_news += 2
        # print(all_news)
        self.conditional_probability = self.conditional_probability / all_news
        self.not_conditional_probability = (1 - self.conditional_probability) * 10000
        self.conditional_probability *= 10000
        #print(self.conditional_probability)
        # print(self.not_conditional_probability)

        pass

    def train(self):
        # 计算条件概率  拉普拉斯平滑
        for i in range(self.category_num):
            for j in range(self.feature_num):

                count_0 = self.conditional_probability[i][j][0]
                count_1 = self.conditional_probability[i][j][1]

                # 计算0，1对应的条件概率
                probalility_0 = (float(count_0) + 1) / (float(count_0 + count_1) + 2) * 100
                probalility_1 = (float(count_1) + 1) / (float(count_0 + count_1) + 2) * 100

                self.conditional_probability[i][j][0] = probalility_0
                self.conditional_probability[i][j][1] = probalility_1
        return None

    def _calculate_probability(self, obj, category):
        """
        计算某个对象属于某个分类的概率
        :param obj:      1维 特征数据集
        :param category: int 分类
        :return: int 概率
        """

        # 获取对应的先验概率
        probability = int(self.prior_probability[category])
        # print(category,probability)
        # 性能优化
        # 根据obj的特征情况（0,1），决定取 该分类存在该特征的概率 还是 该分类不存在该特征的概率
        # all_pro = np.where(obj, self.conditional_probability[category], 1-self.conditional_probability[category])
        # 将 所有条件概率相乘（一维），再乘该分类的先验概率；
        # np.prod(all_pro) * probability

        # 获取所有特征的条件概率
        index = 0
        for feature in obj:
            # 如果有这个特征
            if feature == 1:
                # if index == 2:
                    # print(self.conditional_probability[category][index])
                probability *= int(self.conditional_probability[category][index])
            # 如果没有这个特征
            else:
                # if index == 2:
                    # print(self.conditional_probability[category][index])
                probability *= int(self.not_conditional_probability[category][index])
            index += 1
        return probability

    def predict(self, features):
        """
        批量预测输入数据集的分类
        :param features: 2维 特征数据集
        :return: 分类结果数组
        """

        res = []

        # 如果是批量数据预测
        for obj in features:

            # 重置最大概率为0
            max_category = 0
            max_probability = 0

            # 循环每个分类，求出最大概率
            for cate in range(self.category_num):
                probability = self._calculate_probability(obj, cate)
                # print(probability)


                if probability > max_probability:
                    max_probability = probability
                    max_category = cate
            # print(max_probability)
            # 添加到结果数组中
            res.append(max_category)

        return res

        return None


