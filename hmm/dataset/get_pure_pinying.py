


pure_pinyin = open('./dic2.txt','w',encoding='utf-8')
with open('./dict.txt','r',encoding='utf-8') as f:
    data = f.readlines()
# pinyin_list = []
# for line in data:
#     line = line.strip().split('	')
#     assert len(line) == 2
#     pinyin_string = line[0]
#     pinyin_string = pinyin_string[:-1]
#     pinyin_list.append(pinyin_string)
# pinyin_list = list(set(pinyin_list))
# for p in pinyin_list:
#     pure_pinyin.write(p + '\n')

temp = ''
word_string = ''
for line in data:
    line = line.strip().split('	')
    assert len(line) == 2
    pinyin_string = line[0]
    pinyin_string = pinyin_string[:-1]
    words = line[1]
    if temp == '':
        temp = pinyin_string
        word_string += words
    else:
        if pinyin_string == temp:
            word_string += words
        else:
            pure_pinyin.write(temp + ' '+ word_string + '\n')
            temp = ""
            word_string = ""









