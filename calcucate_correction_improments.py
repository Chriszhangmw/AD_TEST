
import json
import jieba
import numpy
from pypinyin import lazy_pinyin
import matplotlib.pyplot as plt
import numpy as np
import gc
from pyinstrument import Profiler
from hmm_correction import ModelLanguage,GetSymbolDict,GetLanguageModel

dict_pinyin = GetSymbolDict('./hmm/dataset/dict_dialect.txt')
model1 = GetLanguageModel('./hmm/model_language/language_model1.txt')
model2 = GetLanguageModel('./hmm/model_language/language_model2.txt')
ml = ModelLanguage('./hmm/model_language',dict_pinyin,model1,model2)
stopwords = [line.strip() for line in open('./hmm/dataset/stopwords.txt', 'r', encoding='utf-8').readlines()]


class PinyinSimilarity:

    # def __init__(self):
    #     self.ml = ModelLanguage('./hmm/model_language')
    #     self.ml.LoadModel()
    #     self.stopwords = [line.strip() for line in open('./hmm/dataset/stopwords.txt','r',encoding='utf-8').readlines()]
    #


    def _match_not_continue(self,str_input_pinyin,answer_pinyin):
        match = True
        for pinying in answer_pinyin:
            if pinying not in str_input_pinyin:
                return False
        return match

    def get_correction_sentence(self,str_input):
        cutted_word = []
        str_input_list = jieba.lcut(str_input)
        if len(str_input_list) > 10:#返回太长，多半是胡说八道，直接过滤了
            return ""
        str_input_list = list(set(str_input_list))
        str_input_list = [w for w in str_input_list if w not in stopwords]
        for word in str_input_list:
            word_pinyin = lazy_pinyin(word)
            try:
                r = ml.SpeechToText(word_pinyin)
                gc.collect()
                cutted_word.append(r)
            except:
                cutted_word.append(word)

        cutted_word = ''.join(cutted_word)
        return cutted_word

    def answer_match(self,str_input,answer):
        #答案太长了，解码时间比较慢，建议分词之后去搜索，然后再合并
        if self.pinyin_similarity(str_input,answer):
            return True
        else:
            # if len(str_input) > 4:
            cutted_word = []
            str_input_list = jieba.lcut(str_input)
            if len(str_input_list) > 10:  # 返回太长，多半是胡说八道，直接过滤了
                return False
            str_input_list = list(set(str_input_list))
            str_input_list = [w for w in str_input_list if w not in stopwords]
            for word in str_input_list:
                word_pinyin = lazy_pinyin(word)
                try:
                    r = ml.SpeechToText(word_pinyin)
                    cutted_word.append(r)
                except:
                    cutted_word.append(word)
            cutted_word = ''.join(cutted_word)
            return self.pinyin_similarity(cutted_word, answer)


    def pinyin_similarity(self, str_input,answer):
        self.answer_hanzi = answer
        self.answer_pinyin = lazy_pinyin(answer)
        str_input = self._change_word_signal(str_input)
        str_input_hanzi = str_input

        # 如果答案直接在识别文本中，直接返回true
        if self.answer_hanzi in str_input_hanzi:
            return True
        # 拼音进行模糊匹配
        str_input_pinyin = lazy_pinyin(str_input)
        if self._match_not_continue(str_input_pinyin,self.answer_pinyin):
            return True
        str_input_hanzi = []
        for i, char_input_pinyin in enumerate(str_input_pinyin):
            char_input_hanzi = self._match_word(char_input_pinyin)
            if char_input_hanzi:
                char_input_hanzi = list(set(char_input_hanzi))
                str_input_hanzi.append(char_input_hanzi)
            else:
                str_input_hanzi.append([str_input[i]])
        # print(str_input_hanzi)
        str_all_hanzi = self.all_output_hanzi(str_input_hanzi)
        for str_hanzi in str_all_hanzi:
            if self.answer_hanzi in str_hanzi:
                return True
            else:
                return False

    def _change_word_signal(self, str_input):
        str_output = str_input
        str_output = str_output.replace("，", "")
        str_output = str_output.replace("。", "")
        str_output = str_output.replace(" ", "")
        str_output = str_output.replace("？", "")
        return str_output

    def _match_word(self, char_pinyin):
        # 拼音精准匹配
        if char_pinyin in self.answer_pinyin:
            return [self.answer_hanzi[i] for i, x in enumerate(self.answer_pinyin) if x == char_pinyin]
        char_pinyin_head = self._match_head(char_pinyin)  # 替换声母
        if char_pinyin_head in self.answer_pinyin:
            return [self.answer_hanzi[i] for i, x in enumerate(self.answer_pinyin) if x == char_pinyin_head]
        char_pinyin_tail = self._match_tail(char_pinyin)  # 替换韵母
        if char_pinyin_tail in self.answer_pinyin:
            return [self.answer_hanzi[i] for i, x in enumerate(self.answer_pinyin) if x == char_pinyin_tail]
        char_pinyin_head_tail = self._match_tail(char_pinyin_head)  # 都替换
        if char_pinyin_head_tail in self.answer_pinyin:
            return [self.answer_hanzi[i] for i, x in enumerate(self.answer_pinyin) if x == char_pinyin_head_tail]
        # 未替换成功
        return None

    def _match_head(self, char_pinyin):
        if char_pinyin[:2] == 'zh':
            replaced_char_pinyin = char_pinyin.replace('zh', 'z')
        elif char_pinyin[:2] == 'ch':
            replaced_char_pinyin = char_pinyin.replace('ch', 'c')
        elif char_pinyin[:2] == 'sh':
            replaced_char_pinyin = char_pinyin.replace('sh', 's')
        elif char_pinyin[0] == 'z':
            replaced_char_pinyin = char_pinyin.replace('z', 'zh')
        elif char_pinyin[0] == 'c':
            replaced_char_pinyin = char_pinyin.replace('c', 'ch')
        elif char_pinyin[0] == 's':
            replaced_char_pinyin = char_pinyin.replace('s', 'sh')
        elif char_pinyin[0] == 'l':
            replaced_char_pinyin = char_pinyin.replace('l', 'n')
        elif char_pinyin[0] == 'n':
            replaced_char_pinyin = char_pinyin.replace('n', 'l')
        else:
            return char_pinyin
        return replaced_char_pinyin

    def _match_tail(self, char_pinyin):
        if char_pinyin[-3:]=='ang':
            replaced_char_pinyin = char_pinyin.replace('ang', 'an')
        elif char_pinyin[-3:]=='eng':
            replaced_char_pinyin = char_pinyin.replace('eng', 'en')
        elif char_pinyin[-3:]=='ing':
            replaced_char_pinyin = char_pinyin.replace('ing', 'in')
        elif  char_pinyin[-2:]=='an':
            replaced_char_pinyin = char_pinyin.replace('an', 'ang')
        elif char_pinyin[-2:]=='en':
            replaced_char_pinyin = char_pinyin.replace('en', 'eng')
        elif  char_pinyin[-2:]=='in':
            replaced_char_pinyin = char_pinyin.replace('in', 'ing')
        else:
            return char_pinyin
        return replaced_char_pinyin

    def all_output_hanzi(self, input_str):
        if not input_str:
            return list()

        def backtrack(index: int):
            if index == len(input_str):
                combinations.append("".join(combination))
            else:
                for str2 in input_str[index]:
                    combination.append(str2)
                    backtrack(index + 1)
                    combination.pop()

        combinations = list()
        combination = list()
        backtrack(0)
        return combinations

def get_dic(path):
    with open(path,'r',encoding='utf-8') as f:
        dic = json.load(f)
    return dic


def compute(answer,text2,tool):
    if "||" in answer:  # 一个问题，可能有多个答案的
        textList = answer.split('||')
        # new_text = tool.get_correction_sentence(text2)
        for t in textList:
            if tool.answer_match(text2, t): #不加HMM做纠正
                return True
    else:
        if tool.answer_match(text2, answer):
            return  True
    return False

def compute2(answer,text2,tool):
    if "||" in answer:  # 一个问题，可能有多个答案的
        textList = answer.split('||')
        for t in textList:
            if tool.pinyin_similarity(text2, t): #不加HMM做纠正
                return True
    else:
        if tool.pinyin_similarity(text2, answer):
            return True
    return False



def decrease_badlist(compute_number_bad,wrong_catalog,type):
    assert compute_number_bad>0
    num1 = compute_number_bad
    num2 = wrong_catalog.count(type)
    # if type == "compute":
    if wrong_catalog.count(type) == 0:
        return wrong_catalog,0
    elif wrong_catalog.count(type)>0 and wrong_catalog.count(type) < compute_number_bad:
        while wrong_catalog.count(type) > 0:
            wrong_catalog.remove(type)
        return wrong_catalog,num2
    else: #wrong_catalog.count(type) >= compute_number_bad
        while compute_number_bad > 0:
            wrong_catalog.remove(type)
            compute_number_bad -= 1
        return wrong_catalog, num1

def decrease_wronglist(compute_number_wrong,wrong_catalog,type):
    assert compute_number_wrong>0
    num1 = compute_number_wrong
    num2 = wrong_catalog.count(type)
    # if type == "compute":
    if wrong_catalog.count(type) == 0:
        return wrong_catalog,0
    elif wrong_catalog.count(type)>0 and wrong_catalog.count(type) < compute_number_wrong:
        while wrong_catalog.count(type) > 0:
            wrong_catalog.remove(type)
        return wrong_catalog,num2
    else: #wrong_catalog.count(type) >= compute_number_bad
        while compute_number_wrong > 0:
            wrong_catalog.remove(type)
            compute_number_wrong -= 1
        return wrong_catalog, num1


from tqdm import tqdm
def get_report2(dic1,dic2):
    tool = PinyinSimilarity()
    report = {}
    all_question  =0
    all_right = 0
    for k,v in tqdm(dic1.items()):#answer
        #prediction
        report_detail = {}
        total_question = 0
        predict_right_question = 0
        predictions = dic2[k]
        wrong_catalog = []
        for catalog,text in tqdm(v.items()):
            if catalog != 'score' and catalog != 'bad_wav' and catalog != 'wrong_answer':
                predict_text = predictions[catalog]
                if ',' in text:#表示一段音频实际对应了多个答案
                    answer_list = text.split(',')
                    for answer in answer_list:
                        if_right = compute2(answer,predict_text,tool)
                        if if_right:
                            predict_right_question += 1
                            total_question += 1
                            all_question += 1
                            all_right += 1
                        else:
                            new_sentence = tool.get_correction_sentence(predict_text)
                            if_right2 = compute2(answer,new_sentence,tool)
                            if if_right2:
                                print('*'*20)
                                predict_right_question += 1
                                total_question += 1
                                all_question += 1
                                all_right += 1
                            else:
                                # print(k, catalog, "---->", predict_text, new_sentence)
                                total_question += 1
                                all_question += 1
                                wrong_catalog.append(catalog)
                else:
                    if_right = compute2(text, predict_text, tool)
                    if if_right:
                        predict_right_question += 1
                        total_question += 1
                        all_question += 1
                        all_right += 1
                    else:
                        new_sentence2 = tool.get_correction_sentence(predict_text)
                        if_right2 = compute2(text, new_sentence2, tool)
                        if if_right2:
                            print('*' * 20)
                            predict_right_question += 1
                            total_question += 1
                            all_question += 1
                            all_right += 1
                        else:
                            # print(k, catalog, "---->", predict_text, new_sentence2)
                            total_question += 1
                            all_question += 1
                            wrong_catalog.append(catalog)
        bad_wav = v["bad_wav"]
        wrong_answer = v["wrong_answer"]
        for catalog, _ in v.items():
            if catalog == "compute":
                compute_list = ["compute", "compute", "compute", "compute", "compute"]
                for c in compute_list:
                    if c in bad_wav:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            all_question -= 1
                            total_question -= 1
                    if c in wrong_answer:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            predict_right_question += 1
                            all_right += 1
            elif catalog == "immediateMemory":
                immediateMemory_list = ["immediateMemory", "immediateMemory", "immediateMemory"]
                for c in immediateMemory_list:
                    if c in bad_wav:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            all_question -= 1
                            total_question -= 1
                    if c in wrong_answer:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            predict_right_question += 1
                            all_right += 1
            elif catalog == "lateMemory":
                lateMemory_list = ["lateMemory", "lateMemory", "lateMemory"]
                for c in lateMemory_list:
                    if c in bad_wav:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            all_question -= 1
                            total_question -= 1
                    if c in wrong_answer:
                        if c in wrong_catalog:
                            wrong_catalog.remove(c)
                            predict_right_question += 1
                            all_right += 1
            else:
                if catalog in bad_wav:
                    if catalog in wrong_catalog:
                        wrong_catalog.remove(catalog)
                        all_question -= 1
                        total_question -= 1
                if catalog in wrong_answer:
                    if catalog in wrong_catalog:
                        wrong_catalog.remove(catalog)
                        predict_right_question += 1
                        all_right += 1

        report_detail["总的问题个数："] = total_question
        report_detail["预测正确问题个数："] = predict_right_question
        report_detail["预测错误问题个数："] = total_question - predict_right_question
        report_detail["哪些问题预测错了："] = ' '.join(wrong_catalog)
        report[k] = report_detail

    report["accurcy"] = float(all_right/all_question)
    report["总共有效question"] = int(all_question)
    with open('dialect_clinical/report_yuyinzhuanxie_hmm.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, sort_keys=True, ensure_ascii=False)

if __name__ == "__main__":
    '''
    dialect_clinical
    '''
    path = './dialect_clinical/answer_bak_c.json'
    answer_dic = get_dic(path)
    # masr_dic = get_dic("./dialect_clinical/asr_20121227.json")
    xunfei_dic = get_dic("./dialect_clinical/asr_yuyinzhuanxie.json")
    # get_report(answer_dic, xunfei_dic,masr_dic)
    get_report2(answer_dic, xunfei_dic)

    '''
    mandarin_normal
    '''
    # path = './mandarin_normal/answer.json'
    # answer_dic = get_dic(path)
    # xunfei_dic = get_dic("./mandarin_normal/iflytek.json")
    # get_report2(answer_dic, xunfei_dic)

    '''
    dialect_normal
    '''
    # path = './dialect_normal/answer.json'
    # answer_dic = get_dic(path)
    # xunfei_dic = get_dic("./dialect_normal/iflytek.json")
    # get_report2(answer_dic, xunfei_dic)

