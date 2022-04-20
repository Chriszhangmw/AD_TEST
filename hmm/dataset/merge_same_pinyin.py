



pure_pinyin = open('./dic3.txt','w',encoding='utf-8')
pinyin_to_words = {}
with open('./dict.txt','r',encoding='utf-8') as f:
    data = f.readlines()
for line in data:
    line = line.strip().split('	')
    assert len(line) == 2
    pinyins = line[0][:-1]
    words = line[1]
    if pinyins not in pinyin_to_words:
        pinyin_to_words[pinyins] = words
    else:
        prior_words = pinyin_to_words[pinyins]
        prior_words += words
        pinyin_to_words[pinyins] = prior_words
print(len(pinyin_to_words))
for k,v in pinyin_to_words.items():
    pure_pinyin.write(k+' '+v+'\n')


print(len(list(set([s.strip() for s in open('./pure_pinyin.csv','r',encoding='utf-8').readlines()]))))







