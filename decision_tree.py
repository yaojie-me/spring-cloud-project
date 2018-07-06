from math import log
import operator


def calc_entropy(labels):
    """
    计算信息熵
    :param labels: 数据集上标签的集合
    :return: 信息熵
    """
    label_num = len(labels)
    label_show_up_times_dict = {}
    for label in labels:
        if label not in label_show_up_times_dict.keys():
            label_show_up_times_dict[label] = 0
        label_show_up_times_dict[label] += 1
    entropy = 0.0
    for key in label_show_up_times_dict:
        prob = float(label_show_up_times_dict[key]) / label_num
        entropy += prob * log(prob, 2)
    return -entropy


def split_data_set(data_set, labels, index, value):
    """
    根据特征所在的位置 index 和特征的值 value, 从原始数据集中分割出那些值等于 value 的子集和标签子集
    :param data_set: 数据集
    :param labels: 数据集上标签的集合
    :param index: 特质所在的位置
    :param value: 特征的值
    :return: 原始数据集中值等于 value 的子集和标签子集
    """
    sub_data_set = []
    sub_labels = []
    fc_index = 0
    for fc in data_set:
        if fc[index] == value:
            tmp = fc[:index]
            tmp.extend(fc[index + 1:])
            sub_data_set.append(tmp)
            sub_labels.append(labels[index])
        fc_index += 1
    return sub_data_set, sub_labels


def select_best_attribute(data_set, labels):
    """
    选择最佳属性
    :param data_set: 数据集
    :param labels: 数据集上标签的集合
    :return: 最佳属性
    """
    # 特征个数
    feature_num = len(data_set[0])
    # 当前数据集的信息熵
    base_entropy = calc_entropy(labels)
    # 最大的信息增益
    max_info_gain = -1
    # 最佳特征所在的索引
    best_feature = -1

    for i in range(feature_num):
        # 当前特征位置上所有值的 list
        feature_value_list = [example[i] for example in data_set]
        # 值去重
        feature_value_set = set(feature_value_list)
        # 此特征的信息熵
        new_entropy = 0.0
        for value in feature_value_set:
            # 获取子集
            sub_data_set, sub_labels = split_data_set(data_set, labels, i, value)
            # 子集占得比例
            prob = float(len(sub_data_set)) / len(data_set)
            # 特征的信息熵加上想要的部分
            new_entropy += prob * calc_entropy(sub_labels)
        # 计算当前特征的信息增益
        info_gain = base_entropy - new_entropy
        if info_gain > max_info_gain:
            # 取最高信息增益和对应的特征
            max_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_count(labels):
    """
    选出所占比例最高的 label
    :param labels: 数据集上标签的集合
    :return: 标签上所占比例最高的 label
    """
    label_count = {}
    for vote in labels:
        if vote not in label_count.keys():
            label_count[vote] = 0
        label_count[vote] += 1
    sorted_class_count = sorted(label_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def decision_tree(data_set, feature_names, labels):
    """
    生成决策树
    :param data_set: 数据集
    :param feature_names: 特征名称(顺序和数据集中特征的顺序保持一致)
    :param labels: 标签
    :return: 决策树
    """
    if labels.count(labels[0]) == len(labels):
        # labels 中所有元素都相同，即类别完全相同，停止划分
        return labels[0]
    if len(data_set[0]) == 1:
        # 如果只有一个特征
        return majority_count(labels)
    # 选出根节点的最佳属性
    best_feature_index = select_best_attribute(data_set, labels)
    best_feature_name = feature_names[best_feature_index]
    tree = {best_feature_name: {}}
    del (feature_names[best_feature_index])
    attr_values = [example[best_feature_index] for example in data_set]
    attr_values_set = set(attr_values)
    for value in attr_values_set:
        sub_data_set, sub_labels = split_data_set(data_set, labels, best_feature_index, value)
        tree[best_feature_name][value] = decision_tree(sub_data_set, best_feature_name, sub_labels)
    return tree
