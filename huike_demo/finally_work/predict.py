#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   predict.py    
@Contact :   971680807@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/30 20:40   蒋竟成      1.0         模型预测
'''

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import pandas as pd
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=15)


def f(rank):
    return rank * 0.1


def gaussian(sigma, mean, rank):
    '''
    计算高斯累积分布
    :param sigma: 排名尺度
    :param mean: 等效最低排名
    :param rank: 输入最低排名
    :return:
    '''
    z = (mean - rank) / sigma
    return norm.cdf(z)


# lin_reg = linear_model.LinearRegression()
# mean_school=None
# poly_reg = PolynomialFeatures(degree=10)
import psycopg2
conn = psycopg2.connect(database='dbschool', user='postgres', password='admin', host='127.0.0.1', port='5432')
def getMinScore():
    # 数据清洗
    # sql = "select name,min,year,average,max,local_province_name from ceexam where local_province_name='贵州'"
    # data = pd.read_csv('ceexam.csv', usecols=['name', 'min', 'year', 'average', 'max', 'local_province_name'])
    # data = data[data['local_province_name'] == '贵州']
    # sql2 = "select score,all_num,year from school_score_gz where type='理科'"
    # data2 = pd.read_csv('school_score_gz.csv')
    # data2 = data2[data2['type'] == '理科']
    #数据读取
    sql = "select name,min,year,average,max from ceexam where local_province_name='贵州'"
    data = pd.read_sql(sql, con=conn)
    sql2="select score,all_num,year from school_score_gz where type='理科'"
    data2=pd.read_sql(sql2, con=conn)
    #数据清洗
    data_all_min_max = data[(~pd.isna(data['min'])) & (~pd.isna(data['max']))]
    d_mean = (data_all_min_max['max'] - data_all_min_max['min']).mean()
    min_none_index = pd.isna(data['min'])
    data_min_none = data[min_none_index]
    data_min_had = data[~min_none_index]
    max_min_none = pd.isna(data['max'])
    data_min_none_max = data_min_none[max_min_none]
    data_min_none_ave = data_min_none[~max_min_none]
    data_min_none_max['min'] = data_min_none_max['average'] - (0.5 * d_mean)
    data_min_none_ave['min'] = data_min_none_ave['max'] - d_mean
    result = pd.concat([data_min_none_max, data_min_none_ave, data_min_had])
    result['min'] = result['min'].apply(lambda x: int(x))
    result['score'] = result['min']
    result2 = pd.merge(result, data2, )[['name', 'year', 'score', 'all_num']]

    global mean_school
    mean_school = result2.groupby(result2['name'])['all_num'].mean()
    mean_school = mean_school.sort_values()
    std_school = result2.groupby(result2['name'])['all_num'].std()
    result2['std'] = result2['name'].apply(lambda x: std_school[x])
    result2 = result2[~pd.isna(result2['std'])]
    # 等效排名
    x = result2['all_num'].values.reshape(-1, 1)  # 每年最低分排名
    y = result2['std'].values.reshape(-1, 1)  # 每年最低分标准差
    # X_ploy = poly_reg.fit_transform(x)
    # lin_reg.fit(X_ploy, y)
    # print(lin_reg.coef_)
    # print(result2)
    # yy=lin_reg.predict(X_ploy)

    # plt.scatter(x, y, c='b')
    # plt.plot(x, f(x), 'r')
    # plt.xlabel('历年排名位次平均值', fontproperties=font)
    # plt.ylabel('历年排名位次的标准差', fontproperties=font)
    # plt.legend(['y=0.1x'], loc='upper right')
    # plt.show()


def pred():
    '''
    考上学校的概率
    :param dist: 目标学校
    :param rank: 真实排名
    :return:
    '''
    l = input('高校名 位次：\n').split()
    rank = float(l[1])
    mean = mean_school[l[0].strip()]
    sigma = f(mean)
    print("历年位次标准差={:.2f},等效位次={:.0f},录取率{:.2f}%".format(sigma, mean, 100 * gaussian(sigma, mean, rank)))


def recomm():
    l = input('位次：\n')
    count = 10
    for k in mean_school.keys():
        v = mean_school[k]
        p = gaussian(f(v), v, float(l))
        if p > 0.99:
            if count == 0:
                break
            print("垫：", k,'\t录取率{:.2f}%'.format(100*p))
            count -= 1
        elif p > 0.9:
            print("保：", k,'\t录取率{:.2f}%'.format(100*p))
        elif p > 0.4:
            print("稳：", k,'\t录取率{:.2f}%'.format(100*p))
        elif p > 0.2:
            print("冲：", k,'\t录取率{:.2f}%'.format(100*p))


if __name__ == '__main__':
    getMinScore()

    print('=' * 40)
    print('1 录取预测')
    print('2 高校推荐')
    print('0 退出')
    print('=' * 40)
    while True:
        l = input('要进行的操作：\n')
        if l == '1':
            pred()
        elif l == '2':
            recomm()
        elif l == '0':
            break
        print('=' * 40)

