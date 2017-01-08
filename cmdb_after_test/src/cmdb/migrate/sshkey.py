from sqlalchemy import *
from config import SSHKEY_DATABASE_URI
from models.user import User
from models.sshkey import Sshkey
from models.host import Host
from models.user_host import UserHost
from models.host_bastion_apply import  HostBastionApply
from models.host_bastion_tasks import  HostBastionTasks
from application import db
import datetime,time

class SshKey():
    def run(self):
        print "=========start========"
        engine = create_engine(SSHKEY_DATABASE_URI, encoding='utf-8',echo=False)
        connection = engine.connect()
        self.migrate_key(connection)
        self.migrate_host_user(connection)
        self.migrate_apply(connection)
        self.update_cmdb_task(connection)
        print "=========end========"

    def migrate_key(self,connection):
        print "=========migrate pubkey to sshkey start  ========"
        db.engine.execute("truncate table sshkey")
        sql = "SELECT a.username,b.pubkey,b.created FROM `user` AS a,pubkey AS b WHERE b.user_id=a.id and b.`status`=1;"
        key_info = connection.execute(sql)
        for item in key_info:
            user_info = User.query.filter(User.name == item.username).first() or 0
            created_time = time.strftime('%Y-%m-%d', time.localtime(item.created))
            if user_info:
                user_id = user_info.id
                target = Sshkey(user_id,item.username,item.pubkey,created_time)
                db.session.add(target)
                db.session.commit()
        print "======migrate pubkey to sshkey finshed end  ===="

    def migrate_apply(self,connection):
        print "=========migrate apply to host_bastion_apply  start ========"
        db.engine.execute("truncate table host_bastion_apply")
        sql = "SELECT a.username,b.description,b.hosts,b.role,b.created FROM `user` as a,apply as b WHERE b.user_id" \
              "=a.id AND b.`status` = 2;"
        apply_info = connection.execute(sql)
        if apply_info:
            for item in apply_info:
                conn = "(" + item.hosts + ")"
                sql = "SELECT name FROM `host` WHERE id in %s;" %conn
                apply_hosts= connection.execute(sql)
                for info in apply_hosts:
                    cmdb_host_info = Host.query.filter(Host.hostname == info.name ).first()
                    if cmdb_host_info:
                        cmdb_hosts_id = cmdb_host_info.id
                        user_info = User.query.filter(User.name == item.username).first()
                        if user_info:
                            uid = user_info.id
                            approve_uid = self.get_superior(uid)
                        if int(item.role) == 7:
                            role = 1
                        if int(item.role) == 5:
                            role = 2
                        if int(item.role) == 4:
                            role = 3
                        staus = 4
                        days = 7
                        created_time = time.strftime('%Y-%m-%d', time.localtime(item.created))
                        target = HostBastionApply(uid,cmdb_hosts_id,role,approve_uid,staus,days,str(item.description),created_time)
                        db.session.add(target)
                        db.session. commit()
        print "=========migrate apply to host_bastion_apply  end ========"


    def update_cmdb_task(self,connection):
        print "===========update cmdb task  start  ========================"
        db.engine.execute("truncate table host_bastion_tasks")
        excute_time = "2015-01-12 00:00:00"
        HostBastionApply_info = HostBastionApply.query.all()
        for item in HostBastionApply_info:
            type = 2
            status = 0
            target = HostBastionTasks(item.id,item.uid,item.host_id,item.role,type,status,excute_time)
            db.session.add(target)
            db.session.commit()
        print "===========update cmdb task  end  =========================="

    def get_superior(self, user_id):
        user = User.query.filter(User.id == user_id).first()
        if 0 < user.p_level < 7 or 0 < user.m_level < 4:
            return self.get_superior(user.superior_id)
        else:
            return user.id

    def migrate_host_user(self,connection):
        print "=========migrate host_user to user_host start ========"
        db.engine.execute("truncate table user_host")
        sql = "SELECT a.username,b.name,c.role,c.created FROM `user` AS a,host AS b,host_user AS c WHERE c.user_id=a.id " \
              "and c.`status`=1 AND c.host_id=b.id;"
        host_user_info = connection.execute(sql)
        for item in host_user_info:
            user_info = User.query.filter(User.name == item.username).first() or 0
            if user_info:
                uid = user_info.id
            host_info = Host.query.filter(Host.hostname == item.name).first() or 0
            role = 0
            created_time = time.strftime('%Y-%m-%d', time.localtime(item.created))
            if host_info:
                host_id = host_info.id
            if int(item.role) == 7:
                role = 1
            if int(item.role) == 5:
                role = 2
            if int(item.role) == 4:
                role = 3
            if role and user_info and host_info:
                status = 1
                target = UserHost(uid,host_id,role,status,created_time)
                db.session.add(target)
                db.session.commit()
        print "=========migrate host_user to user_host end   ========"




