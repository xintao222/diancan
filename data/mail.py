#-*-coding:UTF-8-*-
#!/usr/bin/env python
# Author: yourname@wandoujia.com
# Created Time: 07/26/13 13:50:44
# about:
import requests


def send_message(subject, text, to):
    return requests.post(
        "https://api.mailgun.net/v2/mail-internal.wandoujia.com/messages",
        auth=("api", "key-5br6rwrim18qcnavw7vfxrud2d9sg5r2"),
        data={"from": "mail@wandoujia.com",
              "to": to,
              "subject": subject,
              "text": subject})

def send_gmail(subject, text, to):
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    from email.Header import Header

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    username = 'noreply@wandoujia.com'
    password = '8plK1er3@PRa9'
    server.login(username, password)

    msg = MIMEMultipart()
    text_msg = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_msg)

    for t in to:
        msg['to'] = t
        msg['from'] = 'noreply@wandoujia.com'
        msg['subject'] = Header(subject, 'gb2312')
        server.sendmail(msg['from'], msg['to'], msg.as_string())
    server.close

if __name__ == "__main__":
    to = ["zhida@wandoujia.com"]
    send_message("Test", "test mailgun", to)
    #send_gmail("Test", "test mailgun", to)
