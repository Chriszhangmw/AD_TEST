import json



def get_dic(path):
    with open(path,'r',encoding='utf-8') as f:
        dic = json.load(f)
    return dic

def generate_answer(person_dic):
    # area = "渝中||袁家岗||铜梁||九龙"
    # city= "重庆"
    # compute= "九十三,八十六,七十九,七十二,六十五"
    # day="二十四"
    # floor="十七"
    # immediateMemory= "皮球||气球,国旗,树木"
    # lateMemory= "皮球||气球,国旗,树木"
    # location= "医学院||重庆医科大学附属第一医院||重庆医学院||医院||老年科"
    # month= "十一"
    # namePencil= "铅笔"
    # nameWatch= "手表||钟"
    # reason= "冬"
    # repeat= "大家齐心协力拉紧绳"
    # street= "石油路||友谊路||学院路"
    # week="三"
    # year= "二零二一||二一"
    answer = {
    "area": "渝中||袁家岗||铜梁||九龙",
    "city": "重庆",
    "compute": "九十三||93,八十六||86,七十九||79,七十二||72,六十五||65",
    "day": "十七||17",
    "floor": "十七||17",
    "immediateMemory": "皮球,国旗,树木",
    "lateMemory": "皮球,国旗,树木",
    "location": "医学院||重庆医科大学附属第一医院||重庆医学院||医院||老年科||从医",
    "month": "二||2",
    "namePencil": "铅笔",
    "nameWatch": "手表",
    "reason": "冬",
    "repeat": "大家齐心协力拉紧绳",
    "street": "石油路||友谊路||学院路||从医",
    "week": "四||4",
    "year": "二零二二||二二||2022||22"}
    person_answer = {}
    for name in person_dic.keys():
        person_answer[name] = answer
    with open('answer2.json', 'w', encoding='utf-8') as f:
        json.dump(person_answer, f, indent=2, sort_keys=True, ensure_ascii=False)








if __name__ == '__main__':
    person_dic = get_dic('./normal_putonghua_0217.json')
    generate_answer(person_dic)













