import numpy as np
import scipy


def regression(data_matrix, label):
    """
    回归算法
    :param data_matrix:数据矩阵
    :param label: 标签矩阵
    :return:权值矩阵
    """
    # 数据数量
    data_num = len(data_matrix)
    # 生成全部为 1 的列
    one_col = np.array([1 for i in range(data_num)])
    one_col.resize(len(one_col), 1)
    # 把全为1的列加到原数据的最后一列
    data_matrix = np.concatenate((data_matrix, one_col), axis=1)
    # 转置
    data_matrix_t = scipy.transpose(data_matrix)
    # 转置矩阵和数据矩阵的乘积
    mul_result = data_matrix_t.dot(data_matrix)
    # 乘积的逆
    mul_result_i = np.linalg.inv(mul_result)
    # 权值矩阵
    return mul_result_i.dot(data_matrix_t).dot(label)
