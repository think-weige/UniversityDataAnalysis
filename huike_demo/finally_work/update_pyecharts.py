#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   update_pyecharts.py    
@Contact :   971680807@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/8/1 16:31   唐永金      1.0         数据可视化
'''

#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   demo_pyecharts.py    
@Contact :   971680807@qq.com
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/7/27 10:36   唐永金      1.0         None
'''
from pyecharts.charts import Bar,Line, Page, Pie,Tree,Geo,Funnel
from pyecharts.commons.utils import JsCode
import pandas as pd
from pyecharts.charts import Map
from pyecharts import options as opts
import analysis_data
from pyecharts.globals import ThemeType, ChartType

result_path='result/'

locals=['上海', '重庆', '河北', '贵州', '黑龙江', '河南', '广东', '福建' ,'湖北' ,'四川', '北京', '湖南', '浙江', '山东',
 '江苏', '吉林' ,'陕西' ,'天津', '海南', '辽宁', '江西' ,'甘肃', '云南', '安徽', '山西', '广西', '新疆', '内蒙古',
]
 #'宁夏', '青海', '西藏','香港' ,'澳门']

wid='800px'
hei='600px'
def map_985_211():
    global wid,hei
    df=pd.read_csv('data/211_985.csv')#前39所为985
    df_985=df.iloc[:39]
    df_211 = df.iloc[39:]

    df_985_num=df_985.groupby('所在地').count().iloc[:,0]
    df_211_num = df_211.groupby('所在地').count().iloc[:, 0]

    c = (
        Geo(init_opts=opts.InitOpts(width=wid,height=hei))
            .add_schema(maptype="china")
            .add("985", list(df_985_num.iteritems()),type_=ChartType.HEATMAP)
            .add("211", list(df_211_num.iteritems()),type_=ChartType.HEATMAP)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="985_211全国分布"),
            visualmap_opts=opts.VisualMapOpts(max_=5),
        #     visualmap_opts=opts.VisualMapOpts(is_piecewise=True,pieces=[
        #   {"min":10, "max": 30},
        #   {"min": 5, "max": 10},
        # {"value": 4},
        #   {"value": 3},
        # {"min": 2,"max": 2},
        #   {"value": 1, "label": '1 一枝独秀', "color": 'grey'},
        # ]
        # )
    )
    )
    return c
def bar_min10_guizhou():
    #贵州计算机收分最低的10所985
    all_year=['2018','2017','2015']
    all_type=['211','985']
    min_=[400,500]
    c_all=[]
    for j in range(2):
        for i in all_year:
            min10_985=analysis_data.min_top10(all_type[j], '贵州', i)[['name', 'min']]
            min10_985=min10_985.sort_values('min',ascending=False)
            c = (
                Bar().add_xaxis([x[0] for x in min10_985.values]).add_yaxis(i, [x[1] for x in min10_985.values])
                .reversal_axis()
                .set_global_opts(
                title_opts=opts.TitleOpts(title=i+"贵州省计算机专业收分最低的"+all_type[j]),
                xaxis_opts=opts.AxisOpts(min_=min_[j])
                )
            )
            c_all.append(c)
    return c_all
def map_type():
    global wid, hei
    school_type_local=analysis_data.school_rank()
    c=Map(init_opts=opts.InitOpts(width=wid,height=hei))
    arr_drop=['理工类','综合类','其他','民族类','农林类']
    for key, value in school_type_local.items():
        if key not in  arr_drop:
            c.add(key,list(value.iteritems()),"china")
    c.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=10
        #     is_piecewise=True,
        #     pieces=[
        #     {"min": 8, "max": 20, "color": 'black'},
        #     {"min": 5, "max": 7,"color": '#DC143C'},
        #     {"value": 4,'color':'#00008B'},
        #     {"value": 3,'color':'green'},
        #     {"min": 2, "max": 2},
        #     {"value": 1, "label": '1 一枝独秀','color':'#FFF8DC'},
        # ]
 ),
        title_opts=opts.TitleOpts(title='各类院校全国分布'),legend_opts = opts.LegendOpts(
        #type_="scroll", pos_left="80%", orient="vertical",
        pos_left='150px',
        selected_mode='single'
    )
    )
    return c
def line_gzu_province():
    global wid,hei
    c=Line(init_opts=opts.InitOpts(width=wid,height=hei))
    data=analysis_data.gzu_province()
    years=['2015','2016','2017','2018']
    c.add_xaxis(years)
    for key,value in data.items():
        value_sort=sorted(value,key=lambda x:x[0])
        value2=[x[1] for x in value_sort]
        c.add_yaxis(key,value2)
    c.set_global_opts(
        yaxis_opts=opts.AxisOpts(min_=300),
        title_opts=opts.TitleOpts(title='贵州大学计算机专业分数线走势'),
        legend_opts=opts.LegendOpts(
            # type_="scroll", pos_left="80%", orient="vertical",
            pos_left='300px',
        )
    )
    return c
from pyecharts.charts import WordCloud
def wordcloud_diamond() -> WordCloud:
    global locals
    data=analysis_data.school_rank_part()
    arr_c=[]

    for local in locals:
        data2=data[data['local']==local][['name','hot']]
        print(data2.values)
        c = (
            WordCloud()
            .add("",data2.values , word_size_range=[10, 50])
            .set_global_opts(title_opts=opts.TitleOpts(title=local))
        )
        arr_c.append(c)
    return arr_c
def gzu_major_satisfied():
    data1=analysis_data.gzu_satisfied()
    data1=data1.iloc[:,:5]
    print(data1)
    type_sas={'综合满意度':'all', '办学条件满意度':'facility', '教学质量满意度':'teaching', '就业满意度':'job'}
    c = Bar()
    for a in type_sas:
        c.add_xaxis([str(x) for x in data1['major'].values])
        c.add_yaxis(a,[x for x in data1[type_sas[a]].values])
        c.set_global_opts(
            yaxis_opts=opts.AxisOpts(min_=3),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10, interval=0)),datazoom_opts=opts.DataZoomOpts())
        c.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                ]
            ),
            markline_opts=opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="average", name="平均值"),
                ]
            ),
        )
    return c
def enroll():
    global wid, hei
    data=analysis_data.enroll_rate()
    data['true_rate']=data['true_rate'].apply(lambda x:float(x)*10)
    print(data['year'].values)
    c = (
        Line(init_opts=opts.InitOpts(width=wid,height=hei))
            .add_xaxis([x for x in data['year'].values])
            .add_yaxis('报名人数', data['num_people'].values, is_smooth=True
                       ,markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]))
            .add_yaxis("实际录取人数", data['true_num'].values, is_smooth=True,
                        markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),)
            .add_yaxis("实际录取率", [round(x,2) for x in data['true_rate'].values], is_smooth=True,
                       markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max")]),)
            .set_global_opts(title_opts=opts.TitleOpts(title="全国高考走势图"))
    )

    return c
def gz_score():
    data1 = analysis_data.line_gz_score()
    years = ['2019', '2018', '2017']
    type=['理科','文科']
    bin = list(range(0, 700, 40))
    c = Bar()
    for a in years:
        for b in type:
            data=data1.copy()
            data=data[(data['year']==a)&(data['type']==b)]
            score = data['score']
            s = pd.cut(score, bin)
            data['bin'] = s.values
            data2=data.groupby('bin').sum()['num']
            c.add_xaxis([str(x) for x in data2.index.categories])
            c.add_yaxis(a+'-'+b,data2.values.tolist())

    c.set_global_opts(
            title_opts=opts.TitleOpts(title="贵州一分一段表分区间图"),
            datazoom_opts=opts.DataZoomOpts(),
            legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            )
        )
    return c
def tree__cs_level():
    data=analysis_data.get_cs_level()
    c = (
        Tree(init_opts=opts.InitOpts(height='3500px'))
            .add("", data,label_opts=opts.LabelOpts(position='insideRight'))
            .set_global_opts(title_opts=opts.TitleOpts(title="计科学科评估树"))
    )
    return c
def map_cs_level():
    global wid, hei
    levels = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-']
    data=analysis_data.get_cs_level_raw()
    c=Map(init_opts=opts.InitOpts(width=wid,height=hei))
    for i in levels:
        c.add(i,data[i],"china")
    c.set_global_opts(
        visualmap_opts=opts.VisualMapOpts(min_=0, max_=5),
        legend_opts=opts.LegendOpts(selected_mode='single'),
        title_opts=opts.TitleOpts(title="计科学科评估")
    )
    return c
def bar_gap():
    '''
    211,985分差top
    :return:
    '''
    data=analysis_data.get_gap()
    data=data.groupby(['level','name']).median().round(2)
    type=['211','985']
    res=[]
    for a in type:
        data_211=data.loc[a]
        data_211=data_211.sort_values('gap',ascending=False).head(10)
        c=Bar()
        c.add_xaxis([x for x in data_211.index.values])
        c.add_yaxis(a,[x[0] for x in data_211.values])
        c.set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10,interval=0))
                          ,title_opts=opts.TitleOpts(title=a+"学校最高分最低分分差top10"))

        res.append(c)
    return res
def pie_level():
    '''
    获知每年 一本 二本 三本 专科 211 985学校变化
    :return:
    '''
    levels=['211','985','专科批','本科一批','本科二批','本科三批']
    years=['2014','2015','2016','2017','2018']
    data=analysis_data.get_level()
    res=[]
    for year in years:
        data1=data[data['year']==year]
        data1=data1.groupby('level').count()
        data1=data1.loc[levels]['name']
        c = (
            Pie(init_opts=opts.InitOpts(width='300px',height='300px'))
                .add(year, list(data1.iteritems()))
                .set_global_opts(title_opts=opts.TitleOpts(title=year+"计算机专业开设情况"
                ),legend_opts=opts.LegendOpts(
                type_="scroll", pos_left="80%", orient="vertical"
            ))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        res.append(c)
    return res

def woman_985_top10():
    data_raw=analysis_data.get_sex_985()
    levels=['985','211']
    womens={'硕士女生数':'shuo_woman'}
    res=[]
    for level in levels:
        data=data_raw[data_raw['level']==level]
        for key,value in womens.items():
            data1=data.sort_values(value,ascending=False).head(10)[['name',value]]
            # c = (
            #     Pie(init_opts=opts.InitOpts(height='300px'))
            #         .add('', [list(x) for x in data1.values])
            #         .set_global_opts(title_opts=opts.TitleOpts(title=level+'\n'+key ),
            #                          legend_opts=opts.LegendOpts(
            #     type_="scroll", pos_left="80%", orient="vertical"
            # ),)
            #         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            # )
            print([list(x) for x in data1.values])
            c = (
                Funnel()
                    .add(
                    "商品",
                    [list(x) for x in data1.values],
                    label_opts=opts.LabelOpts(position="inside"),
                )
                    .set_global_opts(title_opts=opts.TitleOpts(title=level+"硕士女生top10"),
                                     legend_opts=opts.LegendOpts(
                                         pos_top='30%',
                                         type_="scroll", pos_left="0%", orient="vertical"
                                     )
                                     )
            )
            print(data1)
            res.append(c)

    return res

def bar_double_one():
    data=analysis_data.getdouble_one()

    c = (
        Bar().add_xaxis([x for x in data['major_type'].values]).add_yaxis('双一流专业',[int(x) for x in data['count'].values] )
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=10, interval=0)),
            datazoom_opts=opts.DataZoomOpts(),

        )
    )
    c.render(result_path+'test.html')
if __name__ == '__main__':
    #bar_double_one()
    '''
    历年高考,报名人数,实际录取,录取率走势图
    985_211地图分布
    计算机专业评估等级全国分布图
    不同种类学校的地图分布
    '''
    page_country = Page(layout=Page.SimplePageLayout)
    page_country.add(enroll())
    page_country.add(map_985_211())
    page_country.add(map_cs_level())
    page_country.add(map_type())
    page_country.render(result_path+'全国型数据.html')
    #词云
    # page_words = Page(layout=Page.SimplePageLayout)
    # arr_wordcloud=wordcloud_diamond()
    # for i in arr_wordcloud:
    #     page_words.add(i)
    # page_words.render(result_path+'各省份学校热度词云图.html')
    '''
    贵州计算机收分最低的985
    贵州计算机收分最低的211
    '''
    # page3=Page(layout=Page.SimplePageLayout)
    # page3.add(gz_score())
    # for i in bar_min10_guizhou():
    #     page3.add(i)
    # page3.render(result_path+'贵州省相关.html')
    '''
    贵州大学计算机专业收分走势
    贵州大学各专业满意度(阳光高考超过250人评价的专业)
    '''
    # page4=Page(layout=Page.SimplePageLayout)
    # page4.add(gzu_major_satisfied())
    # page4.add(line_gzu_province())
    # page4.render(result_path+'贵州大学相关.html')
    '''
    计算机专业评估等级树
    '''
    # c=tree__cs_level()
    # c.render(result_path+'计算机专业评估等级树.html')
    '''
    211,985中计算机专业最低分最高分分差top10
    '''
    # c5=bar_gap()
    # page5=Page(layout=Page.SimplePageLayout)
    # for i in c5:
    #     page5.add(i)
    # page5.render(result_path+'211_985计算机专业最低分最高分分差top10.html')
    '''
    计算机专业(专业中有计算机三个字)不同批次(一本,二本,三本,专科,211,985)学校数量变化
    '''
    # c6=pie_level()
    # page6 = Page(layout=Page.SimplePageLayout)
    # for i in c6:
    #     page6.add(i)
    # page6.render(result_path + '计算机专业各批次变化.html')
    '''
    211,985 女生人数 top10
    '''
    # c7=woman_985_top10()
    # page7 = Page(layout=Page.SimplePageLayout)
    # for i in c7:
    #     page7.add(i)
    #     page7.render(result_path + '985_211女生数据分析.html')