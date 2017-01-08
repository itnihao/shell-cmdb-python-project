# -*- coding: utf-8 -*-
import os,atexit
from signal import signal, SIGTERM
from models.mail_queue import MailQueue
from views.functions import sendmail
from application import db
SENDMAIL_PID_FILE = '/var/run/sendmail.pid'

def atexit_removepid(pid_file):
    try:
        os.remove(pid_file)
    except:
        pass
    print '---------end--------------'

class SendMail:
    def run(self):
        pid_file=SENDMAIL_PID_FILE
        if os.path.isfile(pid_file):
            print("The program is running")
            return 1
        else:
          try:
            signal(SIGTERM, lambda signum, stack_frame: exit(1))
            atexit.register(lambda:atexit_removepid(pid_file))
            fd=os.open(pid_file,os.O_CREAT|os.O_EXCL|os.O_RDWR)
            os.write(fd,"%s\n" % os.getpid())
            os.close(fd)
          except:
            print("Cann't get a lock file")
            return 1
        data = MailQueue.query.filter(MailQueue.status == MailQueue.STATUS_FREE).all()
        if not data:
            return
        for item in data:
            item.status = MailQueue.STATUS_SUCCESS
            db.session.commit()

            subject = item.subject
            html = item.content
            receiver = item.email
            result = sendmail(subject, html, receiver)

            if result == False:
                item.status = MailQueue.STATUS_FAIL
                db.session.commit()