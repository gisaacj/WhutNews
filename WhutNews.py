#coding=utf-8

'爬取武汉理工大学内网的学校通告'

import urllib.request
import re
import time
import smtplib
from email.mime.text import MIMEText

def SendMail(content):
    mail_host = ''
    mail_user = ''
    mail_pass = ''
    sender = ''
    receivers = ['']
    message = MIMEText(content,'plain','utf-8')
    message['Subject'] = '学校最新通知'
    message['Form'] = sender
    message['To'] = receivers[0]
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,25)
        smtpObj.login(mail_user,mail_pass)
        smtpObj.sendmail(
            sender,receivers,message.as_string())
        smtpObj.quit()
        print('success')
    except smtplib.SMTPException as e:
        print('error',e)

def GetNews():
    url = 'http://i.whut.edu.cn/xxtg/'
    page = urllib.request.urlopen(url).read().decode('utf-8')
    p = re.compile(r'<a href="./znbm(.*?)" title="(.*?)"(.*?)</a></span><strong>(.*?)</strong>')
    items = p.findall(page)
    news =[]
    for item in items:
        if(item[3] == time.strftime('%Y-%m-%d',time.localtime(time.time()))):
            news.append([item[1]])
    return news

if __name__ == '__main__':
    before = []
    while True:
        send = []
        news = GetNews()
        content = ''
        for new in news:
            if new not in before:
                send += new
        if send:
            for item in send:
                content += 'notice:'
                content += item
                content += '\r\n'
                before = news
        if content:
            print(content)
            time.sleep(7200)

        
    
