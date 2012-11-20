#!/usr/bin/env python
#-*-coding:utf-8-*-
from email.Header import Header
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
import smtplib
import redis
import time

def send(mail):
    #basename =u"豌豆荚应用推广服务介绍.pdf"
    #创建一个带附件的实例
    msg = MIMEMultipart()
    #构造附件
    #att = MIMEText(open('/home/work/diaochapai/1.pdf', 'rb').read(), 'base64', 'gb2312')
    #att["Content-Type"] = 'application/octet-stream'
    #att["Content-Disposition"] = 'attachment; filename="%s"' % basename.encode('gb2312')
    text = "hi %s，\n两点之前快订餐吧，阿姨很辛苦，拿到订单后还要挨家打电话给餐馆，一打就要打2个多小时，体谅一下阿姨加快订餐速度吧。：）\n 订餐地址: http://fan.wandoulabs.com"%mail.split("@")[0]
    text_msg = MIMEText(text,'plain','utf-8')  
    #msg.attach(att)
    msg.attach(text_msg)
    
    #加邮件头
    msg['to'] = mail
    msg['from'] = 'zhida@wandoujia.com'
    msg['subject'] = Header(u'晚饭是人生大事 迟不得', 'gb2312')
    #发送邮件
    server = smtplib.SMTP('smtp.gmail.com:587')
    username = 'noreply@wandoujia.com'
    password = '8Raq3%DE'
    server.starttls()
    server.login(username,password)
    server.sendmail(msg['from'], msg['to'], msg.as_string())
    server.close

if  __name__ =="__main__":
    c = redis.Redis(host='127.0.0.1', port=6379, db=1)
    people = c.keys("dinner:cname:*")
    str_time = time.strftime("%Y%m%d", time.localtime())
    for p in people:
        mail = p.split(":")[2]
        flag = c.exists("dinner:%s:%s"%(str_time,mail))
        if flag:
            continue
        else:
            if mail.split("@")[1] == "wandoujia.com":
                send(mail)
