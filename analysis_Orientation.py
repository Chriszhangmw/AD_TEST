#
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# plotdata = pd.DataFrame({
#     "iflytek":[65, 60, 88, 54, 85,30],
#     "proposed model":[67, 67, 92, 67, 85,40]},
#     index=['orientation', 'immediateMemory', 'attention and calculation', 'lateMemory', 'naming','read and obey'])
# plotdata.plot(kind='bar', stacked=True,figsize=(15, 8))
#
#
# plt.title("MMSE ability analysis")
# plt.xlabel("ability")
# plt.ylabel("accurcy")
# plt.show()


import json

# with open('./kedaxunfei.json', 'r', encoding='utf-8') as f:
#     dic = json.load(f)

with open('./data/lianhe_20211227.json', 'r', encoding='utf-8') as f:
    dic = json.load(f)
all_cata = ["area","city","compute",
            "day","floor","immediateMemory",
            "lateMemory","location","month",
            "namePencil","nameWatch","reason",
            "repeat","street","week","year"]
Orientation = ["area","city",
            "day","floor",
            "location","month",
            "reason",
           "street","week","year"]

Orientation_num = 0
area_num = 0
city_num = 0
day_num = 0
floor_num = 0
location_num = 0
month_num = 0
season_num = 0
street_num = 0
week_num = 0
year_num = 0
for k,v in dic.items():
    if k != "accurcy" and k!= '总共有效question':
        wrong_cata = v['哪些问题预测错了：']
        wrong_cata_list = wrong_cata.split(' ')
        for cata in wrong_cata_list:
            if cata == "area":
                area_num += 1
            elif cata == "city":
                city_num += 1
            elif cata == "day":
                day_num += 1
            elif cata == "floor":
                floor_num += 1
            elif cata == "location":
                location_num += 1
            elif cata == "month":
                month_num += 1
            elif cata == "reason":
                season_num += 1
            elif cata == "street":
                street_num += 1
            elif cata == "week":
                week_num += 1
            elif cata == "year":
                year_num += 1

print(1-area_num/50,1-city_num/50,
      1-day_num/50,1-floor_num/50,
      1-location_num/50,1-month_num/50,
      1-season_num/50,1-street_num/50,1-week_num/50,1-year_num/50)











