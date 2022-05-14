
import json

with open('./answer_bak.json', 'r', encoding='utf-8') as f:
    dic = json.load(f)

bad = 0
for k,v in dic.items():
    if k != "accurcy" and k!= '总共有效question':
        bad += len(v["bad_wav"])
print("all bad number is :",bad)







