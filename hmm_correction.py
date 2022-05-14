import platform as plat
from hmm.model_language.prior_knownledge import shengmu, shengmu_metrix, yunmu_metrix, yunmu
from pypinyin import lazy_pinyin


import sys


def GetSymbolDict(dictfilename):
    '''
    读取拼音汉字的字典文件
    返回读取后的字典
    '''
    txt_obj = open(dictfilename, 'r', encoding='UTF-8')  # 打开文件并读入
    txt_text = txt_obj.read()
    txt_obj.close()
    txt_lines = txt_text.split('\n')  # 文本分割

    dic_symbol = {}  # 初始化符号字典
    for i in txt_lines:
        list_symbol = []  # 初始化符号列表
        if (i != ''):
            # txt_l=i.split('\t')
            txt_l = i.split(' ')
            pinyin = txt_l[0]
            for word in txt_l[1]:
                list_symbol.append(word)
        dic_symbol[pinyin] = list_symbol

    return dic_symbol

def GetLanguageModel(modelLanFilename):
    '''
    读取语言模型的文件
    返回读取后的模型
    '''
    txt_obj = open(modelLanFilename, 'r', encoding='UTF-8')  # 打开文件并读入
    txt_text = txt_obj.read()
    txt_obj.close()
    txt_lines = txt_text.split('\n')  # 文本分割

    dic_model = {}  # 初始化符号字典
    for i in txt_lines:
        if (i != ''):
            txt_l = i.split('\t')
            if (len(txt_l) == 1):
                continue
            dic_model[txt_l[0]] = txt_l[1]

    return dic_model




class ModelLanguage:  # 语音模型类
    __slots__ = 'slash','modelpath','dict_pinyin','model1','model2'
    def __init__(self, modelpath,dict_pinyin,model1,model2):
        self.modelpath = modelpath
        system_type = plat.system()  # 由于不同的系统的文件路径表示不一样，需要进行判断
        self.dict_pinyin = dict_pinyin
        self.model1 = model1
        self.model2 = model2
        self.slash = ''
        if (system_type == 'Windows'):
            self.slash = '\\'
        elif (system_type == 'Linux'):
            self.slash = '/'
        else:
            print('*[Message] Unknown System\n')
            self.slash = '/'

        if (self.slash != self.modelpath[-1]):  # 在目录路径末尾增加斜杠
            self.modelpath = self.modelpath + self.slash
        pass

    def LoadModel(self):
        # self.dict_pinyin = self.GetSymbolDict('./hmm/dataset/dict_dialect.txt')
        # self.model1 = self.GetLanguageModel(self.modelpath + 'language_model1.txt')
        # self.model2 = self.GetLanguageModel(self.modelpath + 'language_model2.txt')
        # self.two_gram_pinyin = self.GetPinyin(self.modelpath + 'dic_pinyin.txt')
        model = (self.dict_pinyin, self.model1, self.model2)
        return model

    def merger_pinyin(self, syllables, shengmu, possible_shengmu):
        res = []
        for p_s in possible_shengmu:
            temp_pnyin = syllables.replace(shengmu, p_s)
            if temp_pnyin in self.dict_pinyin.keys():
                res.append(temp_pnyin)
        return res


    def get_possible_syllables(self, syllables):
        possible_list_syllables = []
        possible_list_syllables.append(syllables)
        if len(syllables) >= 2:  # 先考虑拼音的整体长度大于等于2的情况
            if syllables[:2] in shengmu_metrix.keys():  # 考虑声母是复合的，比如sh,ch等
                shengmu = syllables[:2]
                yunmu_ = syllables[2:]
                possible_shengmu = shengmu_metrix[shengmu]
                for shengmu1 in possible_shengmu:
                    possible_list_syllables.append(shengmu1 + syllables[2:])
                if syllables[2:] in yunmu_metrix.keys():
                    possible_yunmu = yunmu_metrix[yunmu_]
                    for yunmu1 in possible_yunmu:
                        possible_list_syllables.append(syllables[:2] + yunmu1)
            else:
                if syllables[:1] in shengmu_metrix.keys():
                    shengmu = syllables[:1]
                    possible_shengmu = shengmu_metrix[shengmu]
                    for shengmu2 in possible_shengmu:
                        possible_list_syllables.append(shengmu2 + syllables[1:])
                    yunmu_ = syllables[1:]
                    if yunmu_ in yunmu_metrix.keys():
                        possible_yunmu = yunmu_metrix[yunmu_]
                        for yunmu1 in possible_yunmu:
                            possible_list_syllables.append(syllables[:1] + yunmu1)
        possible_list_syllables = [s for s in possible_list_syllables if s in self.dict_pinyin.keys()]
        possible_list_syllables = list(set(possible_list_syllables))
        return possible_list_syllables

    def SpeechToText(self, list_syllable):
        length = len(list_syllable)
        if (length == 0):  # 传入的参数没有包含任何拼音时
            return ''
        str_result = ''

        tmp_lst_result = self.decode(list_syllable, 0.0)
        str_result = str_result + tmp_lst_result[0][0]
        return str_result

    def decode(self, list_syllable, yuzhi=0.0001):
        list_words = []
        num_pinyin = len(list_syllable)
        # 开始语音解码
        for i in range(num_pinyin):
            ls = ''
            if (list_syllable[i] in self.dict_pinyin):  # 如果这个拼音在汉语拼音字典里的话
                ls = self.dict_pinyin[list_syllable[i]]
                possible_pinyin = self.get_possible_syllables(list_syllable[i])
                if len(possible_pinyin) > 0:
                    for p in possible_pinyin:
                        ls += self.dict_pinyin[p]
            else:
                break
            ls = list(set(ls))
            if (i == 0):
                num_ls = len(ls)
                for j in range(num_ls):
                    tuple_word = ['', 0.0]
                    tuple_word = [ls[j], 1.0]
                    list_words.append(tuple_word)
                continue
            else:
                list_words_2 = []
                num_ls_word = len(list_words)
                for j in range(0, num_ls_word):
                    num_ls = len(ls)
                    for k in range(0, num_ls):
                        tuple_word = ['', 0.0]
                        tuple_word = list(list_words[j])  # 把现有的每一条短语取出来
                        tuple_word[0] = tuple_word[0] + ls[k]  # 尝试按照下一个音可能对应的全部的字进行组合
                        tmp_words = tuple_word[0][-2:]  # 取出用于计算的最后两个字
                        if (tmp_words in self.model2):  # 判断它们是不是再状态转移表里
                            a1 = float(self.model2[tmp_words])
                            a2 = float(self.model1[tmp_words[-2]])
                            tuple_word[1] = tuple_word[1] * a1 / a2
                        else:
                            tuple_word[1] = 0.0
                            continue
                        if (tuple_word[1] >= pow(yuzhi, i)):
                            list_words_2.append(tuple_word)
                list_words = list_words_2
        # list_words = list(set(list_words))
        for i in range(0, len(list_words)):
            for j in range(i + 1, len(list_words)):
                if (list_words[i][1] < list_words[j][1]):
                    tmp = list_words[i]
                    list_words[i] = list_words[j]
                    list_words[j] = tmp

        return list_words


    def GetSymbolDict(self, dictfilename):
        '''
        读取拼音汉字的字典文件
        返回读取后的字典
        '''
        txt_obj = open(dictfilename, 'r', encoding='UTF-8')  # 打开文件并读入
        txt_text = txt_obj.read()
        txt_obj.close()
        txt_lines = txt_text.split('\n')  # 文本分割

        dic_symbol = {}  # 初始化符号字典
        for i in txt_lines:
            list_symbol = []  # 初始化符号列表
            if (i != ''):
                # txt_l=i.split('\t')
                txt_l = i.split(' ')
                pinyin = txt_l[0]
                for word in txt_l[1]:
                    list_symbol.append(word)
            dic_symbol[pinyin] = list_symbol

        return dic_symbol

    def GetLanguageModel(self, modelLanFilename):
        '''
        读取语言模型的文件
        返回读取后的模型
        '''
        txt_obj = open(modelLanFilename, 'r', encoding='UTF-8')  # 打开文件并读入
        txt_text = txt_obj.read()
        txt_obj.close()
        txt_lines = txt_text.split('\n')  # 文本分割

        dic_model = {}  # 初始化符号字典
        for i in txt_lines:
            if (i != ''):
                txt_l = i.split('\t')
                if (len(txt_l) == 1):
                    continue
                dic_model[txt_l[0]] = txt_l[1]

        return dic_model

    def GetPinyin(self, filename):
        file_obj = open(filename, 'r', encoding='UTF-8')
        txt_all = file_obj.read()
        file_obj.close()
        txt_lines = txt_all.split('\n')
        dic_list = []
        for line in txt_lines:
            if (line == ''):
                continue
            pinyin_split = line.split('\t')
            assert len(pinyin_split) == 2
            p1, p2 = pinyin_split[0], pinyin_split[1]
            dic_list.append((p1, p2))
        return dic_list




import gc

if (__name__ == '__main__'):
    dict_pinyin = GetSymbolDict('./hmm/dataset/dict_dialect.txt')
    model1 = GetLanguageModel('./hmm/model_language/language_model1.txt')
    model2 = GetLanguageModel('./hmm/model_language/language_model2.txt')
    ml = ModelLanguage('./hmm/model_language',dict_pinyin,model1,model2)
    # ml.LoadModel()
    # 大家齐心协力拉近神纳
    # str_pinyin = ['da', 'jia', 'ji', 'xin', 'xie', 'li','la','jin','sheng']
    # str_pinyin = ['pi', 'qiao']
    import jieba
    a = '啤酒、国旗、树木'
    b = jieba.lcut(a)
    new = []
    for w in b:
        str_pinyin = lazy_pinyin(w)
        try:
            r = ml.SpeechToText(str_pinyin)

            gc.collect()
            new.append(r)
        # print('语音转文字结果：\n', r)
        except:
            new.append(w)
    print(''.join(new))







