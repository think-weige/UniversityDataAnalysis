import requests
from bs4 import BeautifulSoup




# 城市
city = []
# 学校数量
school_count = []
major_list = []
major_count = []
# 学习专业类型
major_type = []
# 学校专业类型数量
count = []


# 解析各省入选数量
response = requests.get('https://gaokao.koolearn.com/zhuanti/shuangyiliu/')
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, "html.parser")
school_name = soup.select(
    'body > div.main > div:nth-child(2) > div:nth-child(7) > div.table > table:nth-child(1) > tbody > tr > td:nth-child(1)')
print(school_name)
try:
    for i in school_name:
        if not len(i.get_text(strip=True)) > 3:
            if i.get('rowspan') == None:
                counts = 1
                school_count.append(counts)
            else:
                school_count.append(int(i.get('rowspan')))
            city.append(i.get_text(strip=True))
except:
    pass


# 解析学科数量
soup2 = BeautifulSoup(response.text,"html.parser")
school_major1 = soup2.select('body > div.main > div:nth-child(2) > div:nth-child(14) > div.table > table > tr > td:nth-child(2)')
school_major2 = soup2.select('body > div.main > div:nth-child(2) > div:nth-child(14) > div.table > table > tr > td:nth-child(4)')
for major1,major2 in zip(school_major1,school_major2):
    major_list.append(major1.get_text(strip=True))
    major_list.append(major2.get_text(strip=True))
for major1 in major_list:
    for major2 in major1.split("、"):
        major_count.append(major2)
        major_type = list(set(major_count))
for i in major_type:
    count.append(int(major_count.count(i)))



# def analyze_major():
#     pie = Line("双一流高校", "学科名单数量分析",title_pos='center',width=900)
#     #分类
#     pie.add("学科", major_type,count,mark_point = ['min','max'],center=[45,60],is_legend_show=False,is_label_show=True)
#     pie.show_config()
#     pie.render('各高校学科名单数量.html')
#
#
# def analyze_area():
#     map = Map("双一流高校", "各省入选数量分析",title_pos='center',width=900)
#     map.add("", city,school_count,maptype='china', is_visualmap=True, visual_range=[min(school_count), max(school_count)],
#               visual_text_color='#000', is_map_symbol_show=False, is_label_show=True)
#     map.show_config()
#     map.render('各省双一流高校数量.html')
#
# analyze_major()
# analyze_area()

