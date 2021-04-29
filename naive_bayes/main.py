# encoding=utf-8

from bayes_classifier import BayesClassifier
from test_word_matrix import get_test_essay_matrix
from bayes.naive_bayes.utils import *

if __name__ == '__main__':

    print("读取数据-------------------------")
    # 不用读取数据

    print("开始训练-------------------------")
    # 新建分类器对象
    bayes_classifier = BayesClassifier()
    # print(bayes_classifier.prior_probability)
    # print(bayes_classifier.conditional_probability[0][0])
    print("开始测试-------------------------")
    # 读取测试数据

    # 向量化特征
    # features = None
    # cates = None

    # 进行预测
    features = get_test_essay_matrix('../data/测试.xls')
    # print(features[0][1000])
    # print(bayes_classifier.prior_probability.reshape(10, 1))
    # print(bayes_classifier.conditional_probability[0][10:30])
    res = bayes_classifier.predict(features)

    # 结果比较
    # print("分类的正确结果是：", cates)
    # print("预测的分类结果是：", res)

    answer = get_essay_type("../data/测试.xls")
    print(answer)
    print(res)
    print(str('score=')+str(get_score(answer, res)))

    # 获取分类总数
    # workbook = xlrd.open_workbook('../data/源数据.xls')
    #
    # all_news = np.zeros(10)
    # for table in workbook:
    #     all_news[table.number] = table.nrows
    # all_news = all_news[:9]
    # print(all_news)
    # np.save("../model/先验概率矩阵", all_news)





