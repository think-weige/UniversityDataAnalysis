#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   gaokao_craw_data.py    
@Contact :   971680807@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/26 19:39   唐永金      1.0         数据爬取
'''
import requests
import json
import psycopg2
import pandas as pd

def craw(year,num_page):
    url='https://api.eol.cn/gkcx/api/'
    query_string_parameters={
        'keyword':'软件工程',
        'page':num_page,
        'size': 20,
        'uri': 'apidata/api/gk/score/special',
        'year': year
    }
    request_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    s=requests.session()
    res=s.get(url,params=query_string_parameters,headers=request_headers)
    print(res.content.decode('utf-8'))
    return res.content.decode('utf-8')

conn = psycopg2.connect(database='dbschool', user='postgres', password='admin', host='127.0.0.1', port='5432')
cur = conn.cursor()
def insertDb(data):
    df = pd.DataFrame(data)
    columns = ['year','average' ,'min','max', 'local_province_name', 'local_batch_name', 'spname', 'name', 'local_type_name']
    df = df[columns]
    placeholders = ', '.join(['%s'] * df.shape[1])
    columns_str = ', '.join(columns)
    sql = "insert into {}({})values ({})".format('ceexam', columns_str, placeholders)
    cur.executemany(sql,df.values)
    conn.commit()
def craw_school_985_211():
    url='http://www.jinghua.com/exam/newsinfo.jsp'
    s=requests.session()
    res=s.get(url)

    return res.content.decode('gbk')
from lxml import etree
def craw_1fen_1duan():
    url = 'http://kaoshi.edu.sina.com.cn/college/scorelist?tab=file&wl=&local=18&syear=&page='
    for j in range(275):
        page=j+40
        if page>275:
            break
        s = requests.session()
        res = s.get(url+str(page))
        content=res.content.decode('utf-8')
        arr_type=etree.HTML(content).xpath("//table[@class='tbL2']/tr/td/text()")
        length=len(arr_type)-7
        pac=[]
        for i in range(length//6):
            temp=arr_type[7 + i * 6:7 + i * 6 + 6]
            pac.append([temp[2],temp[3],temp[4],temp[5],temp[0]])
        placeholders = ', '.join(['%s'] * 5)
        sql = "insert into {} values ({})".format('school_score_gz', placeholders)
        cur.executemany(sql, pac)
        conn.commit()
        print('第{}页载入成功'.format(page))


if __name__ == '__main__':
    # year=2014
    # num_page=1
    # try:
    #     while True:
    #         data_json=craw(year,num_page)
    #         num_page+=1
    #         data=json.loads(data_json)
    #         data=data['data']['item']
    #         if len(data)==0:
    #             print('{}年数据爬取完毕'.format(year))
    #             year+=1
    #             num_page=1
    #             if year==2019:
    #                 break
    #             else:
    #                 continue
    #         insertDb(data)
    # finally:
    #     conn.close()
    #     cur.close()
    #爬取一分一段表
    #craw_1fen_1duan()
    pass