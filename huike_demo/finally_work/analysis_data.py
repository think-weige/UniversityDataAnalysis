#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   analysis_data.py    
@Contact :   971680807@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/27 11:35   唐永金      1.0         用于数据清洗
'''
import psycopg2
import pandas as pd

conn = psycopg2.connect(database='dbschool', user='postgres', password='admin', host='127.0.0.1', port='5432')
sql_getall='select * from ceexam'
df=pd.read_sql(sql=sql_getall,con=conn)
pd.set_option('display.max_columns', None)
path_data='data/'

def min_top10(level,local_province_name,year):
    school_985=df[(df['level']==level)&(df['min']!=None)&(df['local_province_name']==local_province_name)&(df['year']==year)&(df['local_batch_name']=='本科一批')]
    min_985=school_985.sort_values(['min','year'],ascending=[1,1])
    min_10_985=min_985.head(10)
    return min_10_985
def school_rank()->dict:
    #s数据清洗
    # df_school_rank=pd.read_csv(path_data+'school_rank.csv')
    #     # df_school_rank['major_type'],df_school_rank['rank']=df_school_rank['报名热度排名-类别热度排名'].str.split().str
    #     # df_school_rank.to_csv(path_data+'school_rank_c.csv')
    sql_getall = 'select * from school_rank'
    df_school_rank = pd.read_sql(sql=sql_getall, con=conn)
    arr_type=df_school_rank['major_type'].unique()
    res={}
    for type in arr_type:
        res[type]=df_school_rank[df_school_rank['major_type']==type].groupby('local').count().iloc[:,0]
    return res
def gzu_province():
    provinces=['山东','贵州','福建','江苏','陕西']
    res={}
    for i in provinces:
        res[i]=df[(df['local_province_name']==i)&(df['name']=='贵州大学')][['year','min']].values
    return res
def school_rank_part():
    # data = pd.read_csv(path_data + 'school_hot.csv')
    # data = data[['学校名称', '地区', '人气值']]
    # data['人气值'] = data['人气值'].str.replace('万', '')
    # data.to_csv('data/school_hot2.csv')
    sql='select * from school_hot'
    df_school_rank_part=pd.read_sql(sql=sql,con=conn)
    df_school_rank_part['hot']=df_school_rank_part['hot'].apply(lambda x:int(x))
    return df_school_rank_part
import re
def gzu_satisfied():
    #数据清洗
    # data=pd.read_excel(path_data+'/gzu_satisfied.xlsx')
    # for i in range(2,6):
    #     data['新字段'+str(i)]=[ x[0].strip() for x in data['字段' + str(i)].str.split()]
    #     data['2新字段' + str(i)] = [ re.search(r'\((.*)人\)',x[1]).group(1).strip() for x in data['字段' + str(i)].str.split()]
    #
    # data=data[['字段1','新字段2','新字段3','新字段4','新字段5','2新字段2','2新字段3','2新字段4','2新字段5']]
    # data.to_csv(path_data+'/school_satisfied2.csv')
    # major_name = {'计算机科学与技术': '计科', '采矿工程': '采矿', '机械设计制造及其自动化': '机械', '土木工程': '土木', '电气工程及其自动化': '电气', '英语': '英语',
    #               '法学': '法学'}
    sql = 'select * from school_satisfied'
    data = pd.read_sql(sql=sql, con=conn)
    data['all'] = data['all'].apply(lambda x: round(x, 1))
    data['facility'] = data['facility'].apply(lambda x: round(x, 1))
    data['teaching'] = data['teaching'].apply(lambda x: round(x, 1))
    data['job'] = data['job'].apply(lambda x: round(x, 1))
    data = data[data['num_all'] > 250]
    # data['major'] = data['major'].map(major_name)
    return data
def demo():
    # major_name = {'计算机科学与技术': '计科', '采矿工程': '采矿', '机械设计制造及其自动化': '机械', '土木工程': '土木', '电气工程及其自动化': '电气', '英语': '英语',
    #               '法学': '法学'}
    sql = 'select * from school_satisfied'
    data = pd.read_sql(sql=sql, con=conn)
    data['all'] = data['all'].apply(lambda x: round(x, 1))
    data['facility'] = data['facility'].apply(lambda x: round(x, 1))
    data['teaching'] = data['teaching'].apply(lambda x: round(x, 1))
    data['job'] = data['job'].apply(lambda x: round(x, 1))
    data = data[data['num_all'] > 200]
    #data['major'] = data['major'].map(major_name)
    print(data)
def enroll_rate():
    #数据清洗
    # data=pd.read_csv(path_data+'enroll.csv')
    # data['报名人数']=data['报名人数'].str.replace('万','')
    # data['实际录取人数']=data['实际录取人数'].str.replace('万','')
    # data['实际录取率']=data['实际录取率'].str.replace('%','')
    # data.to_csv(path_data+'enroll2.csv')
    sql = 'select * from enroll'
    data = pd.read_sql(sql=sql, con=conn)
    data=data.sort_values('year')
    return data
def line_gz_score():
    sql = 'select * from school_score_gz'
    data = pd.read_sql(sql=sql, con=conn)
    return data
def get_cs_level():
    sql = 'select * from cs_level'
    data = pd.read_sql(sql=sql, con=conn)
    levels=['A+','A','A-','B+','B','B-','C+','C','C-']
    tree=[{'children':[],'name':'计科学科评估'}]
    for level in levels:
        tree[0]['children'].append({'name': level,'children':[{'name':x} for x in data[data['level'] == level]['name'].values]})
    return tree

def get_cs_level_formap():
    sql='select cs_level.name,cs_level."level",name_local."local" from cs_level,name_local where cs_level."name"=name_local."name"'
    data = pd.read_sql(sql=sql, con=conn)
    sp='<br>'
    data2=data.groupby(['level','local']).agg(lambda x: x.str.cat(sep=sp))
    data2['name']=data2['name'].apply(lambda x:[x.count(sp)+1,x])
    levels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
    res={}
    for i in levels:
        res[i]=list(data2.loc[i].iloc[:, 0].iteritems())
    return res
def get_cs_level_raw():
    sql = 'select cs_level.name,cs_level."level",name_local."local" from cs_level,name_local where cs_level."name"=name_local."name"'
    data = pd.read_sql(sql=sql, con=conn)
    data = data.groupby(['level', 'local']).count()
    levels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
    res = {}
    for i in levels:
        res[i] = list(data.loc[i].iloc[:, 0].iteritems())
    return res



def get_gap():
    sql='select name,level,max-min gap from ceexam where min is not null and max is not null and name in (select name from school_base  )'
    data = pd.read_sql(sql=sql, con=conn)
    return data
def get_level():
    #只考虑一本院校 211正好有10所学校为医科或艺术类院校无计算机专业
    sql="select name,level,year from ceexam "
    data=pd.read_sql(sql=sql,con=conn)
    data=data.drop_duplicates(['name','level','year'])
    return data
def get_sex_985():
    '''
    sex数据中,第二军医大学(211)无数据
    :return:
    '''
    sql="select school_sex.*,school_base.level from school_sex,school_base where school_sex.name=school_base.name"
    data=pd.read_sql(sql,con=conn)
    data=data.round(2)
    return data
def get_company_gzu():
    sql = "select * from school_company"
    data = pd.read_sql(sql, con=conn)
    names=[ 'name'+str(x) for x in list(range(1,11))]
    school_name='贵州大学'
    #data=data[(data['name1']==school_name)|(data['name2']==school_name)|(data['name3']==school_name)|(data['name4']==school_name)|(data['name5']==school_name)|(data['name6']==school_name)|(data['name7']==school_name)|(data['name8']==school_name)|(data['name9']==school_name)|(data['name10']==school_name)]
    res=[]
    for e in data.values:
        if school_name in e:
            res.append({'company':e[0],})
    # data.values
    # print(data)
def getdouble_one():
    data=pd.read_csv(path_data+'li.csv',encoding='gbk')
    return data

# from sklearn.preprocessing import  PolynomialFeatures
# from sklearn import linear_model
#
# from scipy.stats import norm
#
# def gaussian(sigma, mean, rank):
#     '''
#     计算高斯累积分布
#     :param sigma: 排名尺度
#     :param mean: 等效最低排名
#     :param rank: 输入最低排名
#     :return:
#     '''
#     z = (mean-rank) / sigma
#     return norm.cdf(z)
#
# lin_reg = linear_model.LinearRegression()
# mean_school=None
# poly_reg = PolynomialFeatures(degree=5)
# import matplotlib.pyplot as plt
# def getMinScore():
#     #数据清洗
#     sql = "select name,min,year,average,max from ceexam where local_province_name='贵州'"
#     data = pd.read_sql(sql, con=conn)
#     sql2="select score,all_num,year from school_score_gz where type='理科'"
#     data2=pd.read_sql(sql2, con=conn)
#     data_all_min_max=data[(~pd.isna(data['min']))&(~pd.isna(data['max']))]
#     d_mean=(data_all_min_max['max']-data_all_min_max['min']).mean()
#     min_none_index=pd.isna(data['min'])
#     data_min_none=data[min_none_index]
#     data_min_had=data[~min_none_index]
#     max_min_none=pd.isna(data['max'])
#     data_min_none_max=data_min_none[max_min_none]
#     data_min_none_ave=data_min_none[~max_min_none]
#     data_min_none_max['min']=data_min_none_max['average']-(0.5*d_mean)
#     data_min_none_ave['min']=data_min_none_ave['max']-d_mean
#     result=pd.concat([data_min_none_max,data_min_none_ave,data_min_had])
#     result['min']=result['min'].apply(lambda x:int(x))
#     result['score']=result['min']
#     result2=pd.merge(result, data2,)[['name','year','score','all_num']]
#
#     global mean_school
#     mean_school = result2.groupby(result2['name'])['all_num'].mean()
#     std_school=result2.groupby(result2['name'])['all_num'].std()
#     result2 = result2[~pd.isna(result2['all_num'])]
#     result2['std']=result2['name'].apply(lambda x:std_school[x])
#     result2=result2[~pd.isna(result2['std'])]
#     result2=result2[result2['std']<10000]
#     #等效排名
#     x = result2['all_num'].values.reshape(-1, 1)  # 每年最低分排名
#     y = result2['std'].values.reshape(-1, 1)  # 每年最低分标准差
#     X_ploy = poly_reg.fit_transform(x)
#     lin_reg.fit(X_ploy, y)
#     print(lin_reg.coef_)
#     print(result2)
#     yy=lin_reg.predict(X_ploy)
#     plt.scatter(x,y)
#     plt.show()
#
# def f(rank):
#     return rank*0.05
# def pred(dist,rank):
#     '''
#     考上学校的概率
#     :param dist: 目标学校
#     :param rank: 真实排名
#     :return:
#     '''
#     mean=mean_school[dist]
#     # sigma=lin_reg.predict(poly_reg.fit_transform([[mean]]))[0][0]-1000
#     sigma=f(rank)
#     print('sigma={},mean={},rank={}'.format(sigma,mean,rank))
#     print('{:2f}'.format(gaussian(sigma,mean,rank)))

if __name__ == '__main__':
    demo()
    # getMinScore()
    # while True:
    #     l=input().split()
    #     if l=='':
    #         break
    #     pred(l[0].strip(),float(l[1]))
    # conn.close()

