#!/usr/local/bin/python
#-*- coding: UTF-8 -*-
import smtplib
from email.mime.text import MIMEText 
import os,re,sys
import argparse
import logging
import socket
import ast
import urllib2
import datetime

LOG_DIR = "/var/log/zabbix"
SENDER = 'noreply-cmdb@anjuke.com'
SMTP_SERVER = 'smtp.anjuke.com'
USER_NAME = 'noreply-cmdb@anjuke.com'
PASSWORD = 'anjuke2014'
owner_mail = 'pengxie@anjuke.com,18070339080@189.cn'
domain = 'http://192.168.10.130:5000'
apiurl = 'http://192.168.10.130:5000/api/user/'

def get_mail(hostname):
    token_url = apiurl + "hostname:" + hostname
    req = urllib2.Request(token_url)
    response = ""
    data = ""
    try:
        response = urllib2.urlopen(req,timeout=1)
    except urllib2.URLError as e:
        if isinstance(e.reason, socket.timeout):
            subject = "api 超时"
            content = "There was an error: %r \n api timeout" %e
            send_mail(owner_mail,subject,content)
            get_mail(hostname)
        else:
            subject = "The services for api is down"
            content = "There was an error: %r \n %r" %(e,subject)
            send_mail(owner_mail,subject,content)
            sys.exit()
    if response:
        info = ast.literal_eval(response.read())
        if info['errcode'] == 0:
            data = {'email':info['msg'],'hostid':info['hostid'],'hostname':info['hostname']}
        else:
            subject = "api  返回结果出错"
            content = "There was an error: %r" %info
            send_mail(owner_mail,subject,content)
            sys.exit()
    return data

def send_mail(mail_to,subject,content,data=""):
    global sendstatus
    global senderr
    if data:
        hostname = data['hostname']
        hostid   = data['hostid']
        mail_list = mail_to.split(',')
        content= content + "<style type='text/css' > body { font-size: 20px; line-height: 1.5;}</style>"
        href = "<a href='" + str(domain) + "/cmdb/host/" + str(hostid) + "'>" + hostname + "</a>"
        content = re.sub(r'[a-zA-Z0-9]+-[0-9]+',href,content)
        content = content    + "POST TIME = %s " %(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S'))
        content = content + "POST TIME = %s " %(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')) + "<br><br><font style='font-size: 12px;'>如果您不想收到此邮件" \
         "，请点击<a href='" + str(domain) + "/user/alarm?type=email" + "'>退订" + "</a>取消订阅相应主机或pool的报警</font>"
        msg = MIMEText(content,'html','utf8')
        msg['Subject'] = subject
        msg['to'] = ";".join(mail_list)
    try:
        smtp = smtplib.SMTP()
        smtp.connect(SMTP_SERVER)
        smtp.login(USER_NAME,PASSWORD)
        smtp.sendmail(SENDER,mail_list, msg.as_string())
        smtp.close()
        sendstatus = True 
    except Exception,e: 
        senderr=str(e)
        sendstatus = False 

def logwrite(sendstatus,mail_to,content):
    if not sendstatus:
        content = senderr

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    daytime=datetime.datetime.now().strftime('%Y-%m-%d')
    daylogfile=LOG_DIR+'/'+str(daytime)+'.log'
    logging.basicConfig(filename=daylogfile,level=logging.DEBUG)
    logging.debug(str(datetime.datetime.now())+' mail send to {0},content is :\n {1}'.format(mail_to,content))
    cmd = "find %s -type f -ctime +30 -exec rm -f {} \; " %LOG_DIR
    os.system(cmd)


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Send mail to user for zabbix alerting')
    parser.add_argument('mail_to',action="store", help='The address of the E-mail that send to user ')
    parser.add_argument('subject',action="store", help='The subject of the E-mail')
    parser.add_argument('content',action="store", help='The content of the E-mail')
    args = parser.parse_args()
    mail_to=args.mail_to
    subject=args.subject
    content=args.content
    hostname = re.search(r'([a-zA-Z0-9]+-[0-9]+)',subject).group(1)
    if hostname:
        data = get_mail(str(hostname))
        if data['email']:
            email = data['email'] + ',' + mail_to
        else:
            email = mail_to
        send_mail(email,subject,content,data)
        logwrite(sendstatus,mail_to,content)
