

import json



with open('./dialect_clinical/dialect_clinical_report.json', 'r', encoding='utf-8') as f:
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
avg = 0

Orientation_num_model = 0
immediateMemory_num_model = 0
Attention_and_calculation_num_model = 0
lateMemory_num_model = 0
naming_num_model = 0
Read_and_obey_num_model = 0
avg_model = 0

number_people = 0
tatal_questions = 0
for k,v in dic.items():
    if k != "emsemble accurcy" and k!= '总共有效question' and k != "iflytek accurcy":
        number_people += 1
        wrong_cata_ensemble = v["ensemble哪些问题预测错了："]
        wrong_cata_ensemble_list = wrong_cata_ensemble.split(' ')
        temp_emsemble = v["ensemble预测正确问题个数："] / v["总的问题个数："]
        tatal_questions += v["总的问题个数："]
        avg_model += temp_emsemble

        wrong_cata_iflytek = v["iflytek哪些问题预测错了："]
        wrong_cata_iflytek_list = wrong_cata_iflytek.split(' ')
        temp_ilfytek = v["iflytek预测正确问题个数："] / v["总的问题个数："]
        avg += temp_ilfytek

        for cata in wrong_cata_ensemble_list:
            if cata in Orientation:
                Orientation_num_model += 1
            elif cata in immediateMemory:
                immediateMemory_num_model += 1
            elif cata in Attention_and_calculation:
                Attention_and_calculation_num_model += 1
            elif cata in lateMemory:
                lateMemory_num_model += 1
            elif cata in naming:
                naming_num_model += 1
            elif cata in Read_and_obey:
                Read_and_obey_num_model += 1

        for cata in wrong_cata_iflytek_list:
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
        temp = 0
        a1 = 0
        a2 = 0
        a3 = 0
        a4 = 0
        a5 = 0
        a6 = 0

print("*"*10+" iflytek "+"*"*10)
print('Orientation: ',1-Orientation_num/420)
print('immediateMemory: ',1-immediateMemory_num/126)
print('Attention_and_calculation: ',1-Attention_and_calculation_num/210)
print('lateMemory: ',1-lateMemory_num/126)
print('naming: ',1-naming_num/84)
print('Read_and_obey: ',1-Read_and_obey_num/42)
print('number_people: ',number_people)
print('avg accuracy: ',avg/number_people)
print('tatal_questions ',tatal_questions)

print("*"*10+" proposed model "+"*"*10)
print('Orientation: ',1-Orientation_num_model/420)
print('immediateMemory: ',1-immediateMemory_num_model/126)
print('Attention_and_calculation: ',1-Attention_and_calculation_num_model/210)
print('lateMemory: ',1-lateMemory_num_model/126)
print('naming: ',1-naming_num_model/84)
print('Read_and_obey: ',1-Read_and_obey_num_model/42)
print('number_people: ',number_people)
print('avg accuracy: ',avg_model/number_people)
print('tatal_questions ',tatal_questions)











