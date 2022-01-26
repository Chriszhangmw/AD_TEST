import Levenshtein as Lev
from xpinyin import Pinyin

def convert2pinyin(chineseChar):
    p = Pinyin()
    result = p.get_pinyin(chineseChar,)

    s = result.split('-')
    result2 = ' '.join(s)
    return result2
def cer(s1, s2):
    s1, s2, = s1.replace(" ", ""), s2.replace(" ", "")
    return Lev.distance(s1, s2)

a = "嗯是吃饭怎么样吃饭胃口好嗯哈哈哈胃口还不错哈"
b = "等哈儿去吃饭怎么样那吃饭了还不错"
print(cer(a, b))

a_ = convert2pinyin(a)
b_ = convert2pinyin(b)

print(a_)
print(b_)
print(cer(a_, b_))