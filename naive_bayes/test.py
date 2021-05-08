import jieba
import pandas as pd
import numpy as np
from ast import literal_eval
import xlrd
from jieba import analyse


def get_row_col_list_by_file(path):
    row_list = []
    source_data = xlrd.open_workbook('../data/Դ����.xls')
    dist_date = xlrd.open_workbook(path)
    with open('../data/words.txt') as f:
        fd = f.read()
        content = literal_eval(fd)  # ת��Ϊlist���͵�����
    col_list = content  # ������
    dist_sheet = dist_date.sheet_by_index(0)
    for i in range(0, dist_sheet.nrows):  # ���������б�ǩ
        row_list.append(str(i + 1))
    return row_list, col_list, source_data


def get_row_col_list():
    row_list = [0]
    source_data = xlrd.open_workbook('../data/Դ����.xls')
    with open('../data/words.txt') as f:
        fd = f.read()
        content = literal_eval(fd)  # ת��Ϊlist���͵�����
    col_list = content  # ������
    return row_list, col_list, source_data


def sheet_cutting(path):  # �������ݱ�ķִ�
    dist_content_dict = {}
    dist_date = xlrd.open_workbook(path)
    rsheet = dist_date.sheet_by_index(0)
    content = []
    for row in rsheet.get_rows():
        product_column = row[0]  # Ʒ�����ڵ���
        product_value = product_column.value
        content.append(product_value)
    return content


def get_content(string):
    return string


def words_stat():
    row_list, col_list, source_data = get_row_col_list_by_file('../data/����.xls')  # ��������м�������
    word_group = {}  # �������ߺ���
    content = col_list  # ������
    word_dict = sheet_cutting()
    i = 0
    for dict in word_dict:
        i = i + 1
        for train_word in content:
            if train_word in dict:
                word_group[str(i) + ',' + str(train_word)] = 1
    return word_group


def words_stat_by_str(string):
    row_list, col_list, source_data = get_row_col_list()  # ��������м�������
    word_group = {}  # �������ߺ���
    content = col_list  # ������
    for train_word in content:
        if train_word in string:
            word_group[str(0) + ',' + str(train_word)] = 1
    return word_group


def generate_matrix(word_group, matrix):  # Ϊ����ֵ
    for key, value in word_group.items():
        A = key.split(',')[0]
        B = key.split(',')[1]
        Eij = word_group[str(A) + ',' + str(B)]
        # ���¾���
        matrix.loc[A, B] = Eij
    return matrix


def get_matrix_by_file(path):
    row_list, column_list, data = get_row_col_list_by_file(path)  # ��þ������row_list����column_list
    word_group = words_stat()  # ��ùؼ��������������Ӧ�Ķ�ά����
    # �½�һ���վ��󣬳�ֵ��0���
    matrix = pd.DataFrame(np.zeros([len(row_list), len(column_list)], dtype=int, order='C'), columns=column_list,
                          index=row_list)
    # print(matrix)
    matrix = generate_matrix(word_group, matrix)
    return matrix


def get_matrix_by_string(title, content):
    row_list, column_list, data = get_row_col_list()  # ��þ������row_list����column_list
    word_group = words_stat_by_str(content)  # ��ùؼ��������������Ӧ�Ķ�ά����
    # �½�һ���վ��󣬳�ֵ��0���
    matrix = pd.DataFrame(np.zeros([len(row_list), len(column_list)], dtype=int, order='C'), columns=column_list,
                          index=row_list)
    # print(matrix)
    matrix = generate_matrix(word_group, matrix)
    return matrix


if __name__ == '__main__':
    matrix = get_matrix_by_file('../data/����.xls')
    print(matrix)
