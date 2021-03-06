#-*- coding: UTF-8 -*-
import StringIO
from fabric.api import *
from fabric.contrib import files
from application import db,app
from models.host_bastion_apply import HostBastionApply
from models.host_bastion_tasks import HostBastionTasks
from models.user_host import UserHost
from models.sshkey import Sshkey
from models.host import Host
from models.ip_address import IpAddress
from models.user import User
from models.mail_queue import MailQueue
from sqlalchemy import and_
import datetime

ROOT_KEY_FILE = '/root/.ssh/authorized_keys'
EVANS_KEY_FILE = '/home/evans/.ssh/authorized_keys'
READONLY_KEY_FILE = '/home/readonly/.ssh/authorized_keys'
DELIMITER_BEGIN = '### Generated by SSH-KEY - BEGIN'
DELIMITER_END = DELIMITER_BEGIN.replace('BEGIN', 'END')

#env.host = '192.168.193.39'
#env.user = 'root'
#env.password = '123456'
env.abort_on_prompts = True
env.time_out = 3

class Bastion_Tasks_Test:
    def run(self):
        print '---------start--------------'
        self.role_root_users = set()
        self.role_evans_users = set()
        self.role_readonly_users = set()
        self.push_key()
        print '---------end--------------'

    def push_key(self):
        now = datetime.datetime.now()
        #task_status = [HostBastionTasks.STATUS_FREE,HostBastionTasks.STATUS_FAIL]
        #current_task = HostBastionTasks.query.filter(and_(HostBastionTasks.status.in_(task_status), HostBastionTasks.exec_time <= now)).first()
        task_status = HostBastionTasks.STATUS_FREE
        current_task = HostBastionTasks.query.filter(HostBastionTasks.id == 783).first()
        if current_task:
            print '------Do Task:%s-----------'%current_task.id
            self.getUids(current_task)
            flag = self.do_task(current_task)
            self.do_apply(current_task.apply_id,flag)
            if flag:
                current_task.status = HostBastionTasks.STATUS_SUCCESS
                self.user_host_mapping(current_task.uid,current_task.host_id,current_task.role,current_task.type)
            else:
                current_task.status = HostBastionTasks.STATUS_FAIL
            db.session.commit()

    def getUids(self,current_task):
        if current_task.type == HostBastionTasks.TYPE_ADD:
            self.setUids(current_task.role,current_task.uid)
        else:
            self.user_host_mapping(current_task.uid,current_task.host_id,current_task.role,current_task.type)

        host_users = UserHost.query.filter(and_(UserHost.host_id == current_task.host_id, UserHost.status == UserHost.STATUS_VALID)).all()
        if host_users:
            for host_user in host_users:
                self.setUids(host_user.role,host_user.uid)

    def setUids(self,role,uid):
        if int(role) == UserHost.ROLE_ROOT:
            self.role_root_users.add(uid)
            self.role_evans_users.add(uid)
            self.role_readonly_users.add(uid)

        elif int(role) == UserHost.ROLE_EVANS:
            self.role_evans_users.add(uid)
            self.role_readonly_users.add(uid)

        elif int(role) == UserHost.ROLE_READONLY:
            self.role_readonly_users.add(uid)

    def do_task(self,current_task):
        try:
            params = dict()
            role_root_users = self.role_root_users
            role_evans_users = self.role_evans_users
            role_readonly_users = self.role_readonly_users
            #get ip
            host_info = Host.query.filter(Host.id == current_task.host_id).first()
            ip = self._get_ip(host_info.id)
            env.host = ip
            execute(self.check_remote_file, host=env.host)

            params['key_file'] = ROOT_KEY_FILE
            params['keys'] = self.get_keys(role_root_users)
            self.proceess_task(ip, params, current_task.id)

            #readonly
            params['key_file'] = READONLY_KEY_FILE
            params['keys'] = self.get_keys(role_readonly_users)
            self.proceess_task(ip, params, current_task.id)

            evans_home = execute(self.process_check_evans_home, host=env.host)
            if evans_home[env.host]:
                params['key_file'] = '/home/www/.ssh/authorized_keys'
            else:
                params['key_file'] = EVANS_KEY_FILE

            params['keys'] = self.get_keys(role_evans_users)
            self.proceess_task(ip, params, current_task.id)
            return True
        except:
            return False

    def _get_ip(self,host_id):
        host_info = Host.query.filter(Host.id == host_id).first()
        ip_info = IpAddress.query.filter(IpAddress.id == host_info.primary_ip_id).first()
        return ip_info.ipv4


    def process_check_evans_home(self):
        evans_home = run("cat /etc/passwd| grep evans")
        evans_list = evans_home.split(":")
        if evans_list[5] == '/home/evans':
            return False
        return True

    def get_keys(self,user_ids):
        keys = set()
        root_user_keys = Sshkey.query.filter(Sshkey.uid.in_(user_ids)).all()
        for root_user_key in root_user_keys:
                keys.add(root_user_key.key)
        return keys

    def proceess_task(self,host_ip, params, task_id):
        execute(self.build_host, params, host=env.host)

    def check_remote_file(self):
        self.create_remote_file(ROOT_KEY_FILE, 'root', 'root')
        self.create_remote_file(EVANS_KEY_FILE, 'evans', 'www-data')
        self.create_remote_file(READONLY_KEY_FILE, 'readonly', 'readonly')

    def create_remote_file(self,remote_file, user, group):
        remote_dir = remote_file[0:-16]
        if not files.exists(remote_dir, use_sudo=False, verbose=False):
            run("mkdir -p "+remote_dir+" && chown -R "+user+":"+group+" "+remote_dir+" && chmod 700 "+remote_dir)

        if not files.exists(remote_file, use_sudo=False, verbose=False):
            run("touch "+remote_file+" && chown "+user+":"+group+" "+remote_file+" && chmod 600 "+remote_file)

    def build_host(self,params):
        print 'Build host ip %s, %d keys.' % (env.host, len(params['keys']))
        f_in = StringIO.StringIO()
        get(params['key_file'], f_in)
        f_in.seek(0)  #defaults to 0 (absolute file positioning); other values are 1 (seek relative to the current position) and 2 (seek relative to the file's end).
        f_out = StringIO.StringIO()
        within = False
        for line in f_in:
            if within:
                if line.startswith(DELIMITER_END):
                    within = False

            elif line.startswith(DELIMITER_BEGIN):
                within = True

            else:
                f_out.write(line)
                if not line.endswith('\n'):
                    f_out.write('\n')

        if params['keys']:
            f_out.write(DELIMITER_BEGIN + '\n')
            for key in params['keys']:
                f_out.write(key + '\n' + '\n')
            f_out.write(DELIMITER_END + '\n')

        put(f_out, params['key_file'])

        f_in.close()
        f_out.close()

    def user_host_mapping(self,uid,host_id,role,status):
        hasIn = UserHost.query.filter(and_(UserHost.uid==uid,UserHost.host_id==host_id,UserHost.role==role)).first()
        if status == UserHost.STATUS_VALID:#新增
            if not hasIn:
                target = UserHost(uid,host_id,role,status)
                db.session.add(target)
                db.session.commit()
            else:
                hasIn.status = UserHost.STATUS_VALID
                db.session.commit()

            useremail = User.query.filter(User.id == uid).first()
            email = useremail.email.replace(',', ';')
            subject = "【堡垒机权限】申请成功提示"
            applier = User.query.filter(User.id == uid).first()
            hostname = Host.query.filter(Host.id == host_id).first()
            mail_content = '您申请的主机：' + hostname.hostname + '的权限已开通成功'
            mail_target = MailQueue(email, subject, mail_content, MailQueue.STATUS_FREE)
            db.session.add(mail_target)
            db.session.commit()

        else:#删除
            if hasIn:
                hasIn.status = UserHost.STATUS_OVERDUE
                db.session.commit()

    def do_apply(self,apply_id,flag):
        hasIn = HostBastionApply.query.filter(HostBastionApply.id == apply_id).first()
        if not hasIn:
            return
        if flag:
            hasIn.status = HostBastionApply.STATUS_SUCCESS
        else:
            hasIn.status = HostBastionApply.STATUS_FAIL
        db.session.commit()

