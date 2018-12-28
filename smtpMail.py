#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

my_sender = '277240941@qq.com'  # 发件人邮箱账号
my_pass = 'orwwsdzyqygsbiee'  # 发件人邮箱密码
my_user = '277240941@qq.com'  # 收件人邮箱账号，我这边发送给自己


def mail():
    ret = True
    try:
        # 创建一个带附件的实例
        msg = MIMEMultipart()
        msg['From'] = Header("菜鸟教程", 'utf-8')
        msg['To'] = Header("测试", 'utf-8')
        subject = 'Python SMTP 邮件测试'
        msg['Subject'] = Header(subject, 'utf-8')
        # msg = MIMEText('填写邮件内容', 'plain', 'utf-8')
        # msg['From'] = formataddr(["FromRunoob", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        # msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        # msg['Subject'] = "菜鸟教程发送邮件测试"  # 邮件的主题，也可以说是标题

        # 邮件正文内容
        msg.attach(MIMEText('这是菜鸟教程Python 邮件发送测试……', 'plain', 'utf-8'))

        # 构造附件1，传送当前目录下的 test.txt 文件
        att1 = MIMEText(open('QR.png', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="test.txt"'
        msg.attach(att1)

        # 构造附件2，传送当前目录下的 runoob.txt 文件
        att2 = MIMEText(open('QR.png', 'rb').read(), 'base64', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = 'attachment; filename="runoob.txt"'
        msg.attach(att2)


        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(my_sender, [my_user], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception as e :  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        print(e)
        ret = False
    return ret


ret = mail()
if ret:
    print("邮件发送成功")
else:
    print("邮件发送失败")

    # http: // www.runoob.com / python / python - email.html