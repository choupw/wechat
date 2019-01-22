# -*-encoding:utf-8-*-
import os
import re
import shutil
import time
import itchat
import io
import sys
from itchat.content import *

#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030') #改变标准输出的默认编码
# 说明：可以撤回的有文本文字、语音、视频、图片、位置、名片、分享、附件

# {msg_id:(msg_from,msg_to,msg_time,msg_time_rec,msg_type,msg_content,msg_share_url)}
msg_dict = {}

# 文件存储临时目录
rev_root_dit = "d:/wechat/"
rev_tmp_dir = rev_root_dit + "tmpfile/"
rev_recall_dst = rev_root_dit + "recall/"
rev_msg_log = rev_root_dit + "msg/"
login_user = "1"

if not os.path.exists(rev_root_dit): os.mkdir(rev_root_dit)
if not os.path.exists(rev_tmp_dir): os.mkdir(rev_tmp_dir)
if not os.path.exists(rev_recall_dst): os.mkdir(rev_recall_dst)
if not os.path.exists(rev_msg_log): os.mkdir(rev_msg_log)

# 表情有一个问题 | 接受信息和接受note的msg_id不一致 巧合解决方案
face_bug = None

# 作者：AlicFeng
# 链接：https://www.jianshu.com/p/712d19374b2e
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

# 将接收到的消息存放在字典中，当接收到新消息时对字典中超时的消息进行清理 | 不接受不具有撤回功能的信息
# [TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS, NOTE]
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO])
def handler_receive_msg(msg):
    global face_bug
    # 获取的是本地时间戳并格式化本地时间戳 e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 消息ID
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 消息发送人昵称 | 这里也可以使用RemarkName备注　但是自己或者没有备注的人为None
    msg_from = (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    # 消息接受人昵称
    msg_to = (itchat.search_friends(userName=msg['ToUserName']))["NickName"]
    # 消息内容
    msg_content = None
    # 分享的链接
    msg_share_url = None
    if msg['Type'] == 'Text' \
            or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' \
            or msg['Type'] == 'Attachment' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Picture':
        msg_content = r"" + msg['FileName']
        # 保存文件
        msg['Text'](rev_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content
    # 更新字典
    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )
    # print("msg_time:"+msg_time +"msg_from:"+ msg_from+ "msg_type:"+ msg["Type"]+ " msg_content:"+ msg_content)


    print("msg_time:" +msg_time_rec + "msg_from:" + msg_from + "msg_type:" + msg["Type"] + " msg_content:" + msg_content)
    # 保存记录
    log_msg_user = msg_from
    if msg_from == login_user:
        log_msg_user = msg_to
    log_msg_content = msg_time_rec+" " + msg_from + ": "+msg_content
    write_chat_msg(rev_msg_log + log_msg_user + "-user-chat.txt", log_msg_content)

# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
# 处理群消息
@itchat.msg_register([TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO], isGroupChat=True)
def group_text_reply(msg):
    global face_bug
    # 获取的是本地时间戳并格式化本地时间戳 e: 2017-04-21 21:30:08
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 消息ID
    msg_id = msg['MsgId']
    # 消息时间
    msg_time = msg['CreateTime']
    # 消息来源群名称
    msg_from_group = msg['User']['NickName']
    # 消息发送人昵称 | 这里也可以使用RemarkName备注　但是自己或者没有备注的人为None
    msg_from_user = msg['ActualNickName']

    msg_from = '在群：（ ' + msg_from_group + '）里， 成员：（' +msg_from_user + '）'
    # (itchat.search_friends(userName=msg['FromUserName']))["NickName"]
    # 消息内容
    msg_content = None
    # 分享的链接
    msg_share_url = None
    if msg['Type'] == 'Text' \
            or msg['Type'] == 'Friends':
        msg_content = msg['Text']
    elif msg['Type'] == 'Recording' \
            or msg['Type'] == 'Attachment' \
            or msg['Type'] == 'Video' \
            or msg['Type'] == 'Picture':
        msg_content = r"" + msg['FileName']
        # 保存文件
        msg['Text'](rev_tmp_dir + msg['FileName'])
    elif msg['Type'] == 'Card':
        msg_content = msg['RecommendInfo']['NickName'] + r" 的名片"
    elif msg['Type'] == 'Map':
        x, y, location = re.search(
            "<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
        if location is None:
            msg_content = r"纬度->" + x.__str__() + " 经度->" + y.__str__()
        else:
            msg_content = r"" + location
    elif msg['Type'] == 'Sharing':
        msg_content = msg['Text']
        msg_share_url = msg['Url']
    face_bug = msg_content
    # 更新字典
    msg_dict.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )

    print("msg_time:" +msg_time_rec+  " msg_from:" + msg_from + "msg_type:" + msg["Type"] + " msg_content:" + msg_content)
    # 保存记录
    log_msg_content = msg_time_rec + " " + msg_from_user + ": " + msg_content
    write_chat_msg(rev_msg_log + msg_from_group + "-group-chat.txt", log_msg_content)


# 作者：DT0203
# 链接：https://www.jianshu.com/p/5d4de51f5375
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。

# 收到note通知类消息，判断是不是撤回并进行相应操作
@itchat.msg_register([NOTE],isFriendChat=True,isGroupChat=True,isMpChat=True)
def send_msg_helper(msg):
    global face_bug
    if re.search(r"\<\!\[CDATA\[.*撤回了一条消息\]\]\>", msg['Content']) is not None:
        # 获取消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_dict.get(old_msg_id, {})
        if len(old_msg_id) < 11:
            itchat.send_file(rev_tmp_dir + face_bug, toUserName='filehelper')
            os.remove(rev_tmp_dir + face_bug)
        else:
            msg_body = "告诉你一个秘密~" + "\n" \
                       + old_msg.get('msg_from') + " 撤回了 " + old_msg.get("msg_type") + " 消息" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + "撤回了什么！" + "\n" \
                       +  old_msg.get('msg_content')
            # 如果是分享存在链接
            if old_msg['msg_type'] == "Sharing": msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')

            print(msg_body)
            # 将撤回消息发送到文件助手
            itchat.send(msg_body, toUserName='filehelper')
            write_chat_msg(rev_msg_log +  "filehelper.txt", msg_body)
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (rev_tmp_dir + old_msg['msg_content'])
                itchat.send(msg=file, toUserName='filehelper')
                # os.remove(rev_tmp_dir + old_msg['msg_content'])
                saveRecallFile(old_msg['msg_content'])
            # 删除字典旧消息
            msg_dict.pop(old_msg_id)


def saveRecallFile(fileName):
    os.rename(rev_tmp_dir+fileName,rev_recall_dst+fileName)

def write_chat_msg(filename,text_msg):
    # 写数据
    file_object = open(filename, 'a+',encoding="utf8")
    file_object.writelines("\n"+text_msg)
    file_object.close()


def callback(self):
    print("--login start---")
    print(self.storageClass.userName)
    print(self.storageClass.nickName)
    global login_user
    login_user= self.storageClass.nickName

    global rev_tmp_dir
    rev_tmp_dir = rev_tmp_dir + login_user + "/"
    if not os.path.exists(rev_tmp_dir): os.mkdir(rev_tmp_dir)

    global rev_recall_dst
    rev_recall_dst = rev_recall_dst + login_user + "/"
    if not os.path.exists(rev_recall_dst): os.mkdir(rev_recall_dst)

    global rev_msg_log
    rev_msg_log = rev_msg_log + login_user + "/"
    if not os.path.exists(rev_msg_log): os.mkdir(rev_msg_log)

    write_chat_msg(rev_msg_log + login_user+"-login.txt","---login----")

    print("---login end ---")
if not os.path.exists(rev_tmp_dir): os.mkdir(rev_tmp_dir)

if __name__ == '__main__':
    itchat.auto_login(hotReload=True,loginCallback=callback,statusStorageDir='user1.pkl')
    # itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.run()

# 作者：AlicFeng
# 链接：https://www.jianshu.com/p/712d19374b2e
# 來源：简书
# 简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。