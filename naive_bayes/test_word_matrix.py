import jieba
import pandas as pd
import numpy as np
from ast import literal_eval
import xlrd
from jieba import analyse


def get_row_col_list(path):
    row_list = []
    source_data = xlrd.open_workbook('../data/源数据.xls')
    dist_date = xlrd.open_workbook(path)
    with open('../data/words.txt', encoding='utf-8') as f:
        fd = f.read()
        content = literal_eval(fd)  # 转换为list类型的数据
    col_list = content  # 矩阵列
    dist_sheet = dist_date.sheet_by_index(0)
    for i in range(0, dist_sheet.nrows):  # 定义矩阵的列标签
        row_list.append(str(i + 1))
    return row_list, col_list, source_data


def sheet_cutting():  # 测试数据表的分词
    dist_content_dict = {}
    dist_date = xlrd.open_workbook('../data/测试.xls')
    jieba.analyse.set_stop_words('../data/stop_words.txt')
    rsheet = dist_date.sheet_by_index(0)
    content = []
    for row in rsheet.get_rows():
        product_column = row[0]  # 品名所在的列
        product_value = product_column.value
        content.append(product_value)
    return content


def words_stat():
    row_list, col_list, source_data = get_row_col_list('../data/测试.xls')  # 获得行与列及表数据
    word_group = {}  # 两两作者合作
    content = col_list  # 矩阵列
    word_dict = sheet_cutting()
    i = 0
    for dict in word_dict:
        i = i + 1
        for train_word in content:
            if train_word in dict:
                word_group[str(i) + ',' + str(train_word)] = 1
    return word_group


def generate_matrix(word_group, matrix):  # 为矩阵赋值
    for key, value in word_group.items():
        A = key.split(',')[0]
        B = key.split(',')[1]
        Eij = word_group[str(A) + ',' + str(B)]
        # 更新矩阵
        matrix.loc[A, B] = Eij
    return matrix


def get_test_essay_matrix(path):
    print(path)
    row_list, column_list, data = get_row_col_list(path)  # 获得矩阵的行row_list和列column_list
    word_group = words_stat()  # 获得关键词与文章种类对应的二维数组
    # 新建一个空矩阵，初值用0填充
    matrix = pd.DataFrame(np.zeros([len(row_list), len(column_list)], dtype=int, order='C'), columns=column_list,
                          index=row_list)
    # print(matrix)
    matrix = generate_matrix(word_group, matrix)
    # print(row_list)
    return matrix.values


if __name__ == '__main__':
    matrix = get_test_essay_matrix('../data/预测.xls')
    print(matrix)
