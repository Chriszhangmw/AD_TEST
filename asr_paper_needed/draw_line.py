import matplotlib.pyplot as plt



def dram_line_comprason_bad(answer_iflytek,answer_ensemble):
    plt.title('Heavy Cognitive Impairments Consistency Curve')
    number = len(answer_iflytek)
    x_axix = [i for i in range(number)]
    plt.fill_between(x_axix, answer_iflytek, answer_ensemble, color='green', alpha=0.25)
    # plt.plot(x_axix, total_right_questions, color='green', label='MMSE Score', linestyle=':', linewidth=1,
    #          marker='o', markersize=5,
    #          markeredgecolor='black', markerfacecolor='C0')
    plt.plot(x_axix, answer_iflytek, color='red', label='iFkytek', linestyle='--', linewidth=1,
             marker='*', markersize=5,
             markeredgecolor='black', markerfacecolor='C3')
    plt.plot(x_axix, answer_ensemble, color='blue', label='Proposed-Model', linestyle='-.', linewidth=1,
             marker='v', markersize=5,
             markeredgecolor='black', markerfacecolor='C2')
    plt.legend()  # 显示图例
    plt.xlabel('Patients')
    plt.ylabel('Question Number')
    plt.show()

def dram_line_comprason(answer_iflytek,answer_ensemble):
    plt.title('Non-Heavy Cognitive Impairments Consistency Curve')
    number = len(answer_iflytek)
    x_axix = [i for i in range(number)]
    plt.fill_between(x_axix, answer_iflytek, answer_ensemble, color='green', alpha=0.25)
    # plt.plot(x_axix, total_right_questions, color='green', label='MMSE Score', linestyle=':', linewidth=1,
    #          marker='o', markersize=5,
    #          markeredgecolor='black', markerfacecolor='C0')
    plt.plot(x_axix, answer_iflytek, color='red', label='iFkytek', linestyle='--', linewidth=1,
             marker='*', markersize=5,
             markeredgecolor='black', markerfacecolor='C3')
    plt.plot(x_axix, answer_ensemble, color='blue', label='Proposed-Model', linestyle='-.', linewidth=1,
             marker='v', markersize=5,
             markeredgecolor='black', markerfacecolor='C2')
    plt.legend()  # 显示图例
    plt.xlabel('Patients')
    plt.ylabel('Question Number')
    plt.show()


if __name__ == "__main__":
    scores = [22, 21, 3, 3, 17, 22, 2, 13, 21, 23, 26, 26, 23, 13, 22, 14, 12, 18, 19, 17, 28, 20, 21, 27, 13, 24, 20, 26, 5, 27, 20, 24, 24, 24, 24, 24, 24, 24, 24, 24]
    iflyteck = [20, 18, 22, 20, 16, 19, 20, 22, 21, 18, 19, 22, 22, 7, 17, 7, 13, 17, 21, 22, 18, 17, 14, 19, 22, 18, 18, 19, 23, 21, 12, 24, 21, 22, 23, 24, 21, 23, 21, 21]
    ensemble = [20, 20, 22, 21, 17, 19, 20, 22, 21, 18, 19, 22, 22, 7, 18, 7, 13, 18, 22, 22, 20, 18, 18, 19, 22, 21, 19, 21, 23, 22, 14, 24, 21, 23, 24, 24, 22, 24, 22, 22]
    bad_ifly = []
    not_bad_ifly = []
    bad_ensemble = []
    not_bad_ensemble = []
    for score,ifly,my in zip(scores,iflyteck,ensemble):
        if score <= 15:
            bad_ifly.append(ifly)
            bad_ensemble.append(my)
        else:
            not_bad_ifly.append(ifly)
            not_bad_ensemble.append(my)
    dram_line_comprason_bad(bad_ifly,bad_ensemble)
    dram_line_comprason(not_bad_ifly, not_bad_ensemble)












