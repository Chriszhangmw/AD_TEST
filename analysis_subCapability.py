
import json

# with open('./kedaxunfei.json', 'r', encoding='utf-8') as f:
#     dic = json.load(f)

with open('./dialect_normal/report_yuyinzhuanxie.json', 'r', encoding='utf-8') as f:
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
immediateMemory = ["immediateMemory"]
Attention_and_calculation = ['compute']
lateMemory = ['lateMemory']
naming = ["namePencil","nameWatch"]
Read_and_obey = ["repeat"]
Orientation_num = 0
immediateMemory_num = 0
Attention_and_calculation_num = 0
lateMemory_num = 0
naming_num = 0
Read_and_obey_num = 0
for k,v in dic.items():
    if k != "accurcy" and k!= '总共有效question':
        wrong_cata = v['哪些问题预测错了：']
        wrong_cata_list = wrong_cata.split(' ')
        for cata in wrong_cata_list:
            if cata in Orientation:
                Orientation_num += 1
            elif cata in immediateMemory:
                immediateMemory_num += 1
            elif cata in Attention_and_calculation:
                Attention_and_calculation_num += 1
            elif cata in lateMemory:
                lateMemory_num += 1
            elif cata in naming:
                naming_num += 1
            elif cata in Read_and_obey:
                Read_and_obey_num += 1
print(1-Orientation_num/500,1-immediateMemory_num/150,
      1-Attention_and_calculation_num/250,1-lateMemory_num/150,
      1-naming_num/100,1-Read_and_obey_num/50)











