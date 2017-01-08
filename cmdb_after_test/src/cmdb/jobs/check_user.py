# -*- coding: utf-8 -*-
from models.user import User
from models.sshkey import Sshkey
from application import db
from sqlalchemy import and_
import os

class CheckUser:
    def run(self):
        print '---------start--------------'
        self.test()
        print '=========end================'

    def test(self):
        command1 = 'ssh root@10.10.9.100 -t "grep -v "^#" /etc/passwd |cut -f 1 -d:"'
        user_list = os.popen(command1).read()
        print '执行命令:%s'%command1
        sshkey_info = db.session.query(Sshkey.uid,Sshkey.key,User.name,User.status).filter(and_(User.id == Sshkey.uid),(User.status == 0)).all()
        for a in sshkey_info:
            if a.name in user_list:
                continue
            else:
                command2 = 'ssh root@10.10.9.100 -t "useradd -s /bin/bash -m %s && mkdir -p /home/%s/.ssh && chmod 700 /home/%s/.ssh && echo %s >>/home/%s/.ssh/authorized_keys && chmod 600 /home/%s/.ssh/authorized_keys && chown -R %s. /home/%s/.ssh"'%(a.name,a.name,a.name,a.key,a.name,a.name,a.name,a.name)
                check_status = os.system(command2)
                print '执行命令:%s'%command2

