# encoding = utf-8
import hashlib
import base64
import hmac
import json
import os
import wave
from urllib.parse import urlencode
import logging

from wsgiref.handlers import format_date_time
import datetime
from datetime import datetime
import time
from time import mktime
import _thread as thread
import Levenshtein as Lev
def calculate_cer(s1, s2):
    return Lev.distance(s1, s2)

from ws4py.client.threadedclient import WebSocketClient



STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

CHUNK = 1024

CHANNELS = 1
RATE = 16000




class WsParam(object):
    # 初始化
    # 和账号相关的信息
    def __init__(self, AudioFile, APPId="6d0c56ed", APIKey="eac1fc57fce8848869c39d79a2e25c36",
                 APISecret="ZWI0MWU5ZmIzYTBhYzc3ZTY5MDJiNzc5"):
        self.APPId = APPId
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {
            'app_id': self.APPId
        }
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            'domain': 'iat',
            'language': 'zh_cn',
            # 'accent': 'mandarin',  # 选择普通话还是四川话
            'accent': 'lmz',  # 选择普通话还是四川话
            'vinfo': 1,
            'vad_eos': 10000,
            'nbest':5,
            'wbest':5,
            'nunum':0

        }

    # 生成url
    def create_url(self):
        url = 'wss://iat-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = 'host: ' + 'ws-api.xfyun.cn' + '\n'
        signature_origin += 'date: ' + date + '\n'
        signature_origin += 'GET ' + '/v2/iat ' + 'HTTP/1.1'
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = 'api_key="%s", algorithm="%s", headers="%s", signature="%s"' % (
            self.APIKey, 'hmac-sha256', 'host date request-line', signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            'authorization': authorization,
            'date': date,
            'host': 'ws-api.xfyun.cn'
        }
        url = url + '?' + urlencode(v)
        return url


class Recognition(WebSocketClient):
    def __init__(self, url, ws_param):
        super().__init__(url)
        self.ws_param = ws_param
        self.result_text = ''
        self.result_text_temp = ''

    # 收到websocket消息的处理
    def received_message(self, message):
        message = message.__str__()
        try:
            code = json.loads(message)["code"]
            sid = json.loads(message)["sid"]
            if code != 0:
                errMsg = json.loads(message)["message"]
                print("sid:%s call error:%s code is:%s" % (sid, errMsg, code))

            else:
                data = json.loads(message)["data"]["result"]["ws"]
                result = ""
                for i in data:
                    for w in i["cw"]:
                        result += w["w"]
                self.result_text += result

                print("sid:%s call success!,data is:%s" % (sid, json.dumps(data, ensure_ascii=False)))

        except Exception as e:
            print("receive msg,but parse exception:", e)

    # 收到websocket错误的处理
    def on_error(self, error):
        logging.error(error)

    # 收到websocket关闭的处理
    def closed(self, code, reason=None):
        logging.info('语音识别通道关闭' + str(code) + str(reason))

    # 收到websocket连接建立的处理
    def opened(self):
        def run(*args):
            # framesize = 8000
            frameSize = 1280  # 每一帧的音频大小
            intervel = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧

            with open(self.ws_param.AudioFile, "rb") as fp:
                while True:
                    buf = fp.read(frameSize)
                    # 文件结束
                    if not buf:
                        status = STATUS_LAST_FRAME
                    if status == STATUS_FIRST_FRAME:

                        d = {"common": self.ws_param.CommonArgs,
                             "business": self.ws_param.BusinessArgs,
                             "data": {"status": 0, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        d = json.dumps(d)
                        self.send(d)
                        status = STATUS_CONTINUE_FRAME
                    # 中间帧处理
                    elif status == STATUS_CONTINUE_FRAME:
                        d = {"data": {"status": 1, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        self.send(json.dumps(d))
                    # 最后一帧处理
                    elif status == STATUS_LAST_FRAME:
                        d = {"data": {"status": 2, "format": "audio/L16;rate=16000",
                                      "audio": str(base64.b64encode(buf), 'utf-8'),
                                      "encoding": "raw"}}
                        self.send(json.dumps(d))
                        time.sleep(1)
                        break
                    # 模拟音频采样间隔
                    time.sleep(intervel)
            self.close()

        thread.start_new_thread(run, ())


def audio_to_text(AudioFile):
    ws_param = WsParam(AudioFile)
    ws_url = ws_param.create_url()
    ws = Recognition(ws_url, ws_param)
    ws.connect()
    ws.run_forever()
    res = ws.result_text
    return res


def main():
    result = open('xunfei.csv', 'w', encoding='utf-8')
    with open('./test.csv','r',encoding='utf-8') as f:
        data = f.readlines()
        f.close()
    for line in data:
        line = line.strip().split(',')
        wav_path,gold = line[0],line[1]
        # file_path = './A/A/A032.wav'
        res = audio_to_text(wav_path)
        print(res)
        new_line = wav_path + ',' + gold + ',' + res + '\n'
        result.write(new_line)

def main2():
    t = open('./res.csv','w',encoding='utf-8')
    base = './test/'
    for file in os.listdir(base):
        wav_path = base + file
        res = audio_to_text(wav_path)
        t.write(res + '\n')
        print(res)


if __name__ == "__main__":
    # main2()
    path = './test/A319.wav'
    res = audio_to_text(path)
    print(res)
