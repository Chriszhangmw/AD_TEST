import  os
import random
import re
import json


word = open('newword.csv','w',encoding='utf-8')

data = []
# train = open('./train.csv','w',encoding='utf-8')
# dev = open('./dev.csv','w',encoding='utf-8')
# test = open('./test.csv','w',encoding='utf-8')
def getFlist(path):
    with open("./aishell_labels.json", 'r', encoding='utf-8') as load_f:
        load_dict = json.load(load_f)
    print(type(load_dict))
    new_word = []
    for root, dirs, files in os.walk(path):
        for file in files:
            temp = os.path.join(root, file)
            if temp.endswith('txt'):
                fileName = str(file).replace('.txt','')
                fileName = fileName+'.wav'
                with open(temp,'r',encoding='utf-8') as f:
                    transcript = f.readlines()[0]
                    f.close()
                    transcript = transcript.strip().replace('，','')
                    transcript = transcript.strip().replace(',', '')
                    transcript = transcript.strip().replace('\ufeff', '')
                    transcript = transcript.strip().replace('、', '')
                    transcript = transcript.strip().replace('~', '')
                    transcript = transcript.strip().replace('=', '')
                    transcript = transcript.strip().replace('？', '')
                    transcript = transcript.strip().replace('.', '')
                    transcript = transcript.strip().replace('?', '')
                    transcript = transcript.strip().replace('\t', '')
                    transcript = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", transcript)
                wav_path = os.path.join(root, fileName)
                data.append(wav_path+','+transcript+'\n')
                for w in transcript:
                    if w not in load_dict:
                        new_word.append(w)
                # train.write(wav_path+','+transcript+'\n')
    new_word = list(set(new_word))
    for w in new_word:
        word.write(w + '\n')
    print(new_word)


resDir = './A'
getFlist(resDir)
# random.shuffle(data)
# num_sample = len(data)
# dev_num = num_sample * 0.1
# test_num = num_sample * 0.3
# for i,sample in enumerate(data):
#     if i < dev_num:
#         dev.write(sample)
#     elif i >= dev_num and i <  test_num:
#         test.write(sample)
#     else:
#         train.write(sample)






























