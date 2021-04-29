import pandas as pd
import numpy as np
from ast import literal_eval
import xlrd
# import xlwt


def get_row_col_list():
    row_list = []
    data = xlrd.open_workbook('../data/源数据.xls')
    with open('../data/words.txt', encoding='utf-8') as f:
        fd = f.read()
        content = literal_eval(fd)  # 转换为list类型的数据
    col_list = content  # 矩阵列
    i = 1
    for table in data:  # 循环表
        row_list.append(str(i))
        i+=1
    return row_list, col_list, data


def words_stat():
    row_list, col_list, data = get_row_col_list()  # 获得行与列及表数据
    word_group = {}  # 两两作者合作
    content = col_list  # 矩阵列
    for word in content:  # 循环分词库
        for table in data:  # 循环表
            rows = table.nrows  # 表行数
            num = 0
            for i in range(1, rows):  # 循环取出excel表中的每一篇文章，用于判断关键词是否出现在文章中
                line_value = table.row_values(i, 0, None)
                if word in line_value[0]:
                    word_group[str(table.number+1) + ',' + str(word)] = 1 + num  # 统计当前关键词在某一类新闻中出现的频数，存放于二维数组
                    num += 1
    return word_group


def generate_matrix(word_group, matrix):  # 为矩阵赋值
    for key, value in word_group.items():
        A = key.split(',')[0]
        B = key.split(',')[1]
        Eij = word_group[str(A) + ',' + str(B)]
        # 更新矩阵
        matrix.loc[A, B] = Eij
    return matrix


def save_to_csv(matrix,filename):   # 矩阵保存为csv文件
    matrix.to_csv(filename)


def save_to_binary(matrix,filename):    # 矩阵值保存为二进制文件
    matrix = matrix.values
    np.save(filename, matrix)


if __name__ == '__main__':
    row_list, column_list, data = get_row_col_list()  # 获得矩阵的行row_list和列column_list
    word_group = words_stat()  # 获得关键词与文章种类对应的二维数组
    # print(word_group)     #   打印关键词与文章种类对应的二维数组
    # 新建一个空矩阵，初值用0填充
    # print(column_list)
    matrix = pd.DataFrame(np.zeros([len(row_list), len(column_list)], dtype=int, order='C'), columns=column_list,
                          index=row_list)
    matrix = generate_matrix(word_group, matrix)
    print(matrix)
