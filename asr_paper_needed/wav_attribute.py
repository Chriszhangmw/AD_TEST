import wave
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示符号

file = './test/A309.wav'

# 文件读取
wave_read = wave.open(file, mode="rb")

# 返回声音信号的参数(声道数、量化位数、采样频率、采样点数、压缩类型、压缩类型的描述)
params = wave_read.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]

# 读取N个音频数据(以取样点为单位)，返回字符串格式
str_data = wave_read.readframes(nframes)  # ‘\x00\x00....’

# 关闭文件
wave_read.close()

# 将字符串转换为数组，得到一维的short类型的数组
# 如果声音文件是双声道的，则它由左右两个声道的取样交替构成：LR
wave_data = np.fromstring(str_data, dtype=np.short)  # len: 采样点数*2

# 赋值的归一化
wave_data = wave_data * 1.0 / (max(abs(wave_data)))

# 整合左声道和右声道的数据
wave_data = np.reshape(wave_data, [nframes, nchannels])

# 最后通过采样点数和取样频率计算出每个取样的时间
time = np.arange(0, nframes) * (1.0 / framerate)

plt.figure()
# 左声道波形
plt.subplot(2, 1, 1)
plt.plot(time, wave_data[:, 0])
plt.xlabel("时间/s", fontsize=14)
plt.ylabel("幅度", fontsize=14)
plt.title("左声道", fontsize=14)
plt.grid()  # 标尺

plt.subplot(2, 1, 2)
# 右声道波形
plt.plot(time, wave_data[:, 1], c="g")
plt.xlabel("时间/s", fontsize=14)
plt.ylabel("幅度", fontsize=14)
plt.title("右声道", fontsize=14)

plt.tight_layout()  # 紧密布局
plt.show()






import numpy as np
import scipy.io.wavfile
from matplotlib import pyplot as plt

# 读取数据，返回采样率和audio数据,如果是多通道signal为多维向量
file = './test/A309.wav'
sample_rate, signal = scipy.io.wavfile.read(file)  # len: 采样数

signal = signal[:, 0]
original_signal = signal[0:int(1 * sample_rate)]
sample_num = np.arange(len(original_signal))

# 绘图
plt.figure(figsize=(11, 7), dpi=500)
plt.subplot(212)
plt.plot(sample_num / sample_rate, original_signal, color='blue')
plt.xlabel("Time (sec)")
plt.ylabel("Amplitude")
plt.title("1s signal of Voice ")
plt.show()

