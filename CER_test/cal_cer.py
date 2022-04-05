
import Levenshtein as Lev
def calculate_cer(s1, s2):
    return Lev.distance(s1, s2)

s1 = "啊知道了哈好我们下面来最后一遍测试哈"
s2 = "好记到了哈下面我们来最后一遍测试哈"



print(1-calculate_cer(s1,s2)/len(s2))











# with open('./cer_for_general_test.csv','r',encoding='utf-8') as f:
#     data = f.readlines()
# cer = 0.0
# total_car = 0
# number = 0
# for line in data:
#
#     line = line.strip().split(',')
#     gold = line[1]
#     total_car += len(gold)
#     if len(line) == 2:
#         number += 1
#         pre = line[0]
#         cer_temp = calculate_cer(gold,pre)
#         cer_temp = float(cer_temp/len(gold))
#         cer += cer_temp
#         # print(cer_temp)
# print(cer/number)

