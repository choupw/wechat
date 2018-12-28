from aip import AipSpeech
from datetime import datetime


""" 你的 APPID AK SK """
APP_ID = '11539255'
API_KEY = 'zQ189gT9LNPCfhg8dnZKdd5G'
SECRET_KEY = 'Fu03KBVmBOnGOiBe32G96KW7QKusc312'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



# #---------------TTS
# result  = client.synthesis('你好百度,我叫小苏，今天晴转多云，室外35-27度，东北风3-4级，适合穿短袖短裤，注意防晒', 'zh', 1, {
#     'vol': 5,
# })
#
# # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
# if not isinstance(result, dict):
#     with open('/Users/daiwen/PycharmProjects/auido.mp3', 'wb') as f:
#         f.write(result)


# ----------------ASR
# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
totalTime = 0
for eachNum in range(10):
    a = datetime.now()
    # 识别本地文件
    ret = client.asr(get_file_content('/Users/daiwen/PycharmProjects/test.wav'), 'wav', 16000, {
        'dev_pid': 1536,
    })
    b = datetime.now()
    eachTIme = (b-a).microseconds
    print('调用时差:'+str(eachTIme))
    totalTime+= eachTIme
    print(ret)


print('total：'+str(totalTime) + ' avg :' + str(totalTime/10))