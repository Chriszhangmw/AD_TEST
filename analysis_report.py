
import json

import numpy
from pypinyin import lazy_pinyin
import matplotlib.pyplot as plt
import numpy as np


def dram_line_comprason(answer_iflytek,answer_ensemble,total_right_questions):
    plt.title('C-MMSE Question Consistency Curve')
    x_axix = [i for i in range(40)]
    plt.fill_between(x_axix, answer_iflytek, answer_ensemble, color='green', alpha=0.25)
    # plt.fill_between(x_axix, total_right_questions, answer_ensemble, color='red', alpha=0.25)
    plt.plot(x_axix, total_right_questions, color='green', label='Valid Questions', linestyle=':', linewidth=1,
             marker='o', markersize=5,
             markeredgecolor='black', markerfacecolor='C0')
    plt.plot(x_axix, answer_iflytek, color='red', label='iFkytek', linestyle='--', linewidth=1,
             marker='*', markersize=5,
             markeredgecolor='black', markerfacecolor='C3')
    plt.plot(x_axix, answer_ensemble, color='blue', label='Proposed Model', linestyle='-.', linewidth=1,
             marker='v', markersize=5,
             markeredgecolor='black', markerfacecolor='C2')
    plt.legend()  # 显示图例
    plt.xlabel('Patients')
    plt.ylabel('Question Number')
    plt.show()





from hmm_correction import ModelLanguage
class PinyinSimilarity:

    def __init__(self):
        self.ml = ModelLanguage('./hmm/model_language')
        self.ml.LoadModel()


    def _match_not_continue(self,str_input_pinyin,answer_pinyin):
        match = True
        for pinying in answer_pinyin:
            if pinying not in str_input_pinyin:
                return False
        return match

    def match(self,str_input,answer):
        #答案太长了，解码时间比较慢，建议分词之后去搜索，然后再合并
        if self.pinyin_similarity(str_input,answer):
            return True
        else:
            str_pinyin = lazy_pinyin(str_input)
            try:
                r = self.ml.SpeechToText(str_pinyin)
                return self.pinyin_similarity(r,answer)
            except:
                return False

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
    if_right = False
    if "||" in answer:  # 一个问题，可能有多个答案的
        textList = answer.split('||')
        for t in textList:
            # if tool.pinyin_similarity(text2, t): #不加HMM做纠正
            if tool.match(text2,t):
                if_right = True
    else:
        # if tool.pinyin_similarity(text2, answer):
        if tool.match(text2, answer):
            if_right = True
    return if_right

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




def get_report(dic1,dic2,masr_dic):
    tool = PinyinSimilarity()
    report = {}
    all_question  =0
    all_right_emsemble = 0
    all_right_iflytek = 0
    multi_catalog = ["compute","immediateMemory","lateMemory"]
    answer_iflytek = []
    answer_ensemble = []
    scores = []
    total_questions = []
    for k,v in dic1.items():#answer
        #prediction
        report_detail = {}
        predictions = dic2[k] #科大讯飞的
        predictions2 = masr_dic[k]  # gate CNN的
        wrong_catalog_iflytek = []  # 科大讯飞哪些预测错了的
        wrong_catalog_ensemble = []  # 集成模型哪些预测错了的
        answer_iflytek_ = 0
        answer_ensemble_ = 0
        score = v["score"]
        scores.append(score)
        bad_wav = v["bad_wav"]
        wrong_answer = v["wrong_answer"]
        total_question = 24 - len(bad_wav)
        total_questions.append(total_question)
        all_question += total_question
        for catalog,text in v.items():
            if catalog not in multi_catalog:#先不考虑存在多个答案的情况
                if catalog not in bad_wav:#保证bad音频里的就不听了，不参与判断
                    if catalog not in wrong_answer:
                        if catalog != 'score' and catalog != 'bad_wav' and catalog != 'wrong_answer':
                            iFlyTek_text = predictions[catalog]
                            predict_text = predictions[catalog]
                            predict_text += predictions2[catalog]
                            if_right = compute(text, predict_text, tool)
                            if_right_iflytek = compute(text, iFlyTek_text, tool)
                            if if_right:
                                if if_right_iflytek is False:
                                    print(iFlyTek_text,"---->",predictions2[catalog])
                            if if_right_iflytek:
                                answer_iflytek_ += 1
                            else:
                                wrong_catalog_iflytek.append(catalog)
                            if if_right:
                                answer_ensemble_ += 1
                            else:
                                wrong_catalog_ensemble.append(catalog)
        #开始计算multi_catalog中的三个奇葩
        for catalog, text in v.items():
            if catalog == "compute":
                iFlyTek_text = predictions[catalog]
                predict_text = predictions[catalog]
                predict_text += predictions2[catalog]
                answer_list = text.split(',')
                for answer in answer_list:
                    if_right = compute(answer, predict_text, tool)
                    if_right_iflytek = compute(answer, iFlyTek_text, tool)
                    if if_right:
                        if if_right_iflytek is False:
                            print(iFlyTek_text, "---->", predictions2[catalog])
                    if if_right_iflytek:
                        answer_iflytek_ += 1
                    else:
                        wrong_catalog_iflytek.append(catalog)
                    if if_right:
                        answer_ensemble_ += 1
                    else:
                        wrong_catalog_ensemble.append(catalog)
                if bad_wav.count("compute")>0:
                    compute_number_bad = bad_wav.count("compute")
                    wrong_catalog_ensemble,_ = decrease_badlist(compute_number_bad, wrong_catalog_ensemble, "compute")
                    wrong_catalog_iflytek, _ = decrease_badlist(compute_number_bad, wrong_catalog_iflytek,
                                                                         "compute")
                    # answer_iflytek_ += num_right
                    # answer_ensemble_ += num_right
                if wrong_answer.count("compute")>0:
                    compute_number_wrong = wrong_answer.count("compute")
                    wrong_catalog_ensemble,num_right1 = decrease_wronglist(compute_number_wrong, wrong_catalog_ensemble, "compute")
                    wrong_catalog_iflytek, num_right2 = decrease_wronglist(compute_number_wrong, wrong_catalog_iflytek,
                                                                         "compute")
                    answer_iflytek_ += num_right2
                    answer_ensemble_ += num_right1
            elif catalog == "immediateMemory":
                iFlyTek_text = predictions[catalog]
                predict_text = predictions[catalog]
                predict_text += predictions2[catalog]
                answer_list = text.split(',')
                for answer in answer_list:
                    if_right = compute(answer, predict_text, tool)
                    if_right_iflytek = compute(answer, iFlyTek_text, tool)
                    if if_right:
                        if if_right_iflytek is False:
                            print(iFlyTek_text, "---->", predictions2[catalog])
                    if if_right_iflytek:
                        answer_iflytek_ += 1
                    else:
                        wrong_catalog_iflytek.append(catalog)
                    if if_right:
                        answer_ensemble_ += 1
                    else:
                        wrong_catalog_ensemble.append(catalog)
                if bad_wav.count("immediateMemory") > 0:
                    compute_number_bad = bad_wav.count("immediateMemory")
                    wrong_catalog_ensemble, num_right = decrease_badlist(compute_number_bad, wrong_catalog_ensemble, "immediateMemory")
                    wrong_catalog_iflytek, num_right = decrease_badlist(compute_number_bad, wrong_catalog_iflytek,
                                                                         "immediateMemory")
                    # answer_iflytek_ += num_right
                    # answer_ensemble_ += num_right
                if wrong_answer.count("immediateMemory")>0:
                    compute_number_wrong = wrong_answer.count("immediateMemory")
                    wrong_catalog_ensemble,num_right1 = decrease_wronglist(compute_number_wrong, wrong_catalog_ensemble, "immediateMemory")
                    wrong_catalog_iflytek, num_right2 = decrease_wronglist(compute_number_wrong,
                                                                            wrong_catalog_iflytek, "immediateMemory")
                    answer_iflytek_ += num_right2
                    answer_ensemble_ += num_right1
            elif catalog == "lateMemory":
                iFlyTek_text = predictions[catalog]
                predict_text = predictions[catalog]
                predict_text += predictions2[catalog]
                answer_list = text.split(',')
                for answer in answer_list:
                    if_right = compute(answer, predict_text, tool)
                    if_right_iflytek = compute(answer, iFlyTek_text, tool)
                    if if_right:
                        if if_right_iflytek is False:
                            print(iFlyTek_text, "---->", predictions2[catalog])
                    if if_right_iflytek:
                        answer_iflytek_ += 1
                    else:
                        wrong_catalog_iflytek.append(catalog)
                    if if_right:
                        answer_ensemble_ += 1
                    else:
                        wrong_catalog_ensemble.append(catalog)
                if bad_wav.count("lateMemory") > 0:
                    compute_number_bad = bad_wav.count("lateMemory")
                    wrong_catalog_ensemble, num_right = decrease_badlist(compute_number_bad, wrong_catalog_ensemble, "lateMemory")

                    wrong_catalog_iflytek, num_right = decrease_badlist(compute_number_bad, wrong_catalog_iflytek,
                                                                         "lateMemory")
                    # answer_iflytek_ += num_right
                    # answer_ensemble_ += num_right
                if wrong_answer.count("lateMemory")>0:
                    compute_number_wrong = wrong_answer.count("lateMemory")
                    wrong_catalog_ensemble,num_right1 = decrease_wronglist(compute_number_wrong, wrong_catalog_ensemble, "lateMemory")
                    wrong_catalog_iflytek, num_right2 = decrease_wronglist(compute_number_wrong,
                                                                            wrong_catalog_iflytek, "lateMemory")
                    answer_iflytek_ += num_right2
                    answer_ensemble_ += num_right1

        iflytek_rignt_number = total_question - len(wrong_catalog_iflytek)
        ensemble_right_number = total_question - len(wrong_catalog_ensemble)
        answer_iflytek.append(iflytek_rignt_number)
        answer_ensemble.append(ensemble_right_number)
        report_detail["总的问题个数："] = total_question
        report_detail["ensemble预测正确问题个数："] = ensemble_right_number
        report_detail["iflytek预测正确问题个数："] = iflytek_rignt_number
        report_detail["ensemble预测错误问题个数："] = len(wrong_catalog_ensemble)
        report_detail["iflytek预测错误问题个数："] = len(wrong_catalog_iflytek)
        report_detail["ensemble哪些问题预测错了："] = ' '.join(wrong_catalog_ensemble)
        report_detail["iflytek哪些问题预测错了："] = ' '.join(wrong_catalog_iflytek)

        report[k] = report_detail
        all_right_emsemble += ensemble_right_number
        all_right_iflytek += iflytek_rignt_number
    report["emsemble accurcy"] = float(all_right_emsemble / all_question)
    report["iflytek accurcy"] = float(all_right_iflytek/all_question)
    report["总共有效question"] = int(all_question)
    print(total_questions)
    print(scores)
    print(answer_iflytek)
    print(answer_ensemble)
    dram_line_comprason(answer_iflytek, answer_ensemble,total_questions)
    with open('./dialect_clinical/lianhe_20211227.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, sort_keys=True, ensure_ascii=False)


from tqdm import tqdm
def get_report2(dic1,dic2):
    tool = PinyinSimilarity()
    # res = tool.pinyin_similarity("重庆市的沙评吧区", "沙坪坝")
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
        # bad_wav = v["bad_wav"]
        # wrong_answer = v["wrong_answer"]
        for catalog,text in tqdm(v.items()):
            print(k,catalog)
            if catalog != 'score' and catalog != 'bad_wav' and catalog != 'wrong_answer':
                predict_text = predictions[catalog]
                if ',' in text:#表示一段音频实际对应了多个答案
                    answer_list = text.split(',')
                    for answer in answer_list:
                        if_right = compute(answer,predict_text,tool)
                        if if_right:
                            predict_right_question += 1
                            total_question += 1
                            all_question += 1
                            all_right += 1
                        else:
                            total_question += 1
                            all_question += 1
                            wrong_catalog.append(catalog)
                else:
                    if_right = compute(text, predict_text, tool)
                    if if_right:
                        predict_right_question += 1
                        total_question += 1
                        all_question += 1
                        all_right += 1
                    else:
                        all_question += 1
                        total_question += 1
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
    with open('dialect_normal/report_yuyinzhuanxie_hmm.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, sort_keys=True, ensure_ascii=False)

if __name__ == "__main__":
    '''
    dialect_clinical
    '''
    # path = './dialect_clinical/answer_bak.json'
    # answer_dic = get_dic(path)
    # masr_dic = get_dic("./dialect_clinical/asr_20121227.json")
    # xunfei_dic = get_dic("./dialect_clinical/asr_yuyinzhuanxie.json")
    # get_report(answer_dic, xunfei_dic,masr_dic)
    # get_report2(answer_dic, xunfei_dic)

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
    path = './dialect_normal/answer.json'
    answer_dic = get_dic(path)
    # masr_dic = get_dic("./dialect_normal/asr_20121227.json")
    xunfei_dic = get_dic("./dialect_normal/iflytek.json")
    # get_report(answer_dic, xunfei_dic, masr_dic)
    get_report2(answer_dic, xunfei_dic)

