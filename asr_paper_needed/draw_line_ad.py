
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

x_axix = [0,0.1,0.5,1,2,3]
cer = [66.12,63.07,69.03,63.65,63.46,69.54]
f1 = [47.61,50.69,45.88,50.5,52.38,46.01]
bleu1 = [41.73,50.24,34.09,46.98,45.12,30.18]
bleu2 = [32.8,39,27.1,36.83,36.13,24.51]
unigram = [3.2,2.9,3.5,3,2.9,2.9]
bigram = [40.1,41.8,39.3,40.9,35.2,29.7]

plt.title('α Value Influence')
plt.plot(x_axix, cer, color='green', label='CER',linestyle=':', linewidth=1,
        marker='o', markersize=5,
        markeredgecolor='black', markerfacecolor='C0')
plt.plot(x_axix, bleu1, color='red', label='Bleu-1',linestyle='--', linewidth=1,
        marker=',', markersize=5,
        markeredgecolor='black', markerfacecolor='C3')
plt.plot(x_axix, f1, color='skyblue', label='F1 Score',linestyle='-.', linewidth=1,
        marker='v', markersize=5,
        markeredgecolor='black', markerfacecolor='C2')
plt.plot(x_axix, bleu2,  label='Bleu-2',
         linestyle=':', linewidth=1,
         marker='^', markersize=5,
         markeredgecolor='black', markerfacecolor='C1'
         )
plt.plot(x_axix, unigram, color='magenta', label='Unigrams Distinct',linestyle=':', linewidth=1,
        marker='>', markersize=5,
        markeredgecolor='black', markerfacecolor='C5')
plt.plot(x_axix, bigram, color='blue', label='Bigrams Distinct',linestyle=':', linewidth=1,
        marker='<', markersize=5,
        markeredgecolor='black', markerfacecolor='C5')

plt.legend()  # 显示图例

plt.xlabel('α Value in Loss')
plt.ylabel('rate(%)')
plt.show()





