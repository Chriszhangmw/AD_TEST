


newdata = open('./dic_pinyin2.txt','w',encoding='utf-8')
with open('./dic_pinyin.txt','r',encoding='utf-8') as f:
    data = f.readlines()
    f.close()
pairs = []
for line in data:
    line = line.strip().split('	')
    assert len(line) == 2
    pinyins = line[0].split(' ')
    assert len(pinyins) == 2
    p1 = pinyins[0][:-1]
    p2 = pinyins[1][:-1]
    pairs.append((p1,p2))
pairs = list(set(pairs))
print(len(pairs))

for p in pairs:
    p1,p2 = p
    newdata.write(p1+'\t'+p2+'\n')
















