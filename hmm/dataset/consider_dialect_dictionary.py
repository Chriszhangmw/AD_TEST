import json








def get_dic(path):
    with open(path,'r',encoding='utf-8') as f:
        dic = json.load(f)
    return dic
def get_answer_set(path):
    answers = get_dic(path)
    words = []
    for _,v in answers.items():#answer
        for catalog,text in v.items():
            if isinstance(text,str):
                if "," in text:
                    text = text.split(',')
                    for word in text:
                        for w in word:
                            words.append(w)
                elif '||' in text:
                    text = text.split('||')
                    for word in text:
                        for w in word:
                            words.append(w)
                else:
                    for w in text:
                        words.append(w)
    words = list(set(words))
    print(words)
    return words


def clean(words,words_dialect):
    new = []
    for w in words:
        if w in words_dialect:
            new.append(w)
    return ''.join(new)



if __name__ == "__main__":
    path = './answer_bak.json'
    words_dialect = get_answer_set(path)
    pinyin_to_words = {}
    newdata = open('./dict_dialect.txt', 'w', encoding='utf-8')
    with open('./dict.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()
    for line in data:
        line = line.strip().split('	')
        assert len(line) == 2
        pinyins = line[0][:-1]
        words = line[1]
        words = clean(words,words_dialect)
        if pinyins not in pinyin_to_words:
            pinyin_to_words[pinyins] = words
        else:
            prior_words = pinyin_to_words[pinyins]
            prior_words += words
            pinyin_to_words[pinyins] = prior_words
    print(len(pinyin_to_words))
    for k, v in pinyin_to_words.items():
        newdata.write(k + ' ' + v + '\n')







