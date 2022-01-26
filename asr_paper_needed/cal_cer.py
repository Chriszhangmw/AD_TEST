
import Levenshtein as Lev
def calculate_cer(s1, s2):

    return Lev.distance(s1, s2)
from nltk.translate import bleu_score
from nltk.translate.bleu_score import SmoothingFunction
import numpy as np
from collections import Counter


def calc_f1(data):
    golden_char_total = 0.0+1e-5
    pred_char_total = 0.0+1e-5
    hit_char_total = 0.0
    for response, golden_response in data:
        # golden_response = "".join(golden_response).decode("utf8")
        # response = "".join(response).decode("utf8")
        common = Counter(response) & Counter(golden_response)
        hit_char_total += sum(common.values())
        golden_char_total += len(golden_response)
        pred_char_total += len(response)
    p = hit_char_total / pred_char_total
    r = hit_char_total / golden_char_total
    f1 = 2 * p * r / (p + r+1e-5)
    return f1

def bleu(data):
    bleu_1 = []
    bleu_2 = []
    for hyp, ref in data:
        try:
            score = bleu_score.sentence_bleu(
                [ref], hyp,
                smoothing_function=SmoothingFunction().method7,
                weights=[1, 0, 0, 0])
        except:
            score = 0
        bleu_1.append(score)
        try:
            score = bleu_score.sentence_bleu(
                [ref], hyp,
                smoothing_function=SmoothingFunction().method7,
                weights=[0.5, 0.5, 0, 0])
        except:
            score = 0
        bleu_2.append(score)
    bleu_1 = np.average(bleu_1)
    bleu_2 = np.average(bleu_2)
    return bleu_1, bleu_2


def distinct(seqs):
    intra_dist1, intra_dist2 = [], []
    unigrams_all, bigrams_all = Counter(), Counter()
    for seq in seqs:
        unigrams = Counter(seq)
        bigrams = Counter(zip(seq, seq[1:]))
        intra_dist1.append((len(unigrams)+1e-12) / (len(seq)+1e-5))
        intra_dist2.append((len(bigrams)+1e-12) / (max(0, len(seq)-1)+1e-5))

        unigrams_all.update(unigrams)
        bigrams_all.update(bigrams)

    inter_dist1 = (len(unigrams_all)+1e-12) / (sum(unigrams_all.values())+1e-5)
    inter_dist2 = (len(bigrams_all)+1e-12) / (sum(bigrams_all.values())+1e-5)
    intra_dist1 = np.average(intra_dist1)
    intra_dist2 = np.average(intra_dist2)
    return  inter_dist1, inter_dist2,intra_dist1,intra_dist2


F1data = []
predictions = []

with open('./xunfei.csv','r',encoding='utf-8') as f:
    data = f.readlines()
cer = 0.0
total_car = 0
for line in data:
    line = line.strip().split(',')
    gold = line[1]
    total_car += len(gold)
    if len(line) == 2:
        pre = ''
        cer_temp = calculate_cer(gold,pre)
        cer += cer_temp
    else:
        pre = line[2]
        pre = pre.replace('，','')
        pre = pre.replace('。', '')
        pre = pre.replace('？', '')
        pre = pre.replace('1', '一')
        pre = pre.replace('2', '二')
        pre = pre.replace('3', '三')
        pre = pre.replace('4', '四')
        pre = pre.replace('5', '五')
        pre = pre.replace('6', '六')
        pre = pre.replace('7', '七')
        pre = pre.replace('8', '八')
        pre = pre.replace('9', '九')
        pre = pre.replace('0', '零')
        F1data.append((gold, pre))
        predictions.append(pre)
        cer_temp = calculate_cer(gold, pre)
        cer += cer_temp
print(cer/total_car)

f1 = calc_f1(F1data)
bleu_1, bleu_2 = bleu(F1data)
unigrams_distinct, bigrams_distinct, intra_dist1, intra_dist2 = distinct(predictions)
print(f1, bleu_1, bleu_2, unigrams_distinct, bigrams_distinct, intra_dist1, intra_dist2)
