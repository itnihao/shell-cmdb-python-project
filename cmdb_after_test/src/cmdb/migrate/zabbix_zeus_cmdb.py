# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import MIGRATE_DATABSE_URI
from application import db
#from models.alarm imprt Alarm
from models.host import Host
from models.user import User
from models.alarm import Alarm

class ZabbixUser:
    def run(self):
        ignoreusers = ['kaicai','weiliu_g6','gywang','yunlongxiao_g43','OPS','songli','guoanhu','weihuang','kakiezhang','sherryxie','Stamhe','lenyemeng']
        engine = create_engine(MIGRATE_DATABSE_URI, encoding='utf-8',echo=False)
        connection = engine.connect()
        hosts=connection.execute("select a.app_name,b.label,b.user_id,b.owner_id,b.opsuser_id from hosts as a,item as b where a.item_id =b.id").fetchall()
        host_list ={}
        uids = []
        userlist = {}
        if hosts:
            for item in hosts:
                hostname = item.app_name
                if not hostname:
                    hostname = item.label
                host_list[hostname] = [item.user_id,item.owner_id,item.opsuser_id]
                if item.user_id:
                    uids.append(str(item.user_id))
                if item.owner_id:
                    uids.append(str(item.owner_id))
                if item.opsuser_id:
                    uids.append(str(item.opsuser_id))

        if uids:
            uidstr =",".join(uids)
            sql = "select id,user_name,email from user where id in (%s) order by id asc"%uidstr
            users = connection.execute(sql).fetchall()
            for item in users:
                if item.user_name in ignoreusers:
                    continue
                userlist['uid_%s'%item.id]=[item.user_name,item.email]
        ret = []
        if host_list:
            for k,v in host_list.items():
                tmp = {}
                tmp['hostname']= k
                if v[0] and 'uid_%s'%v[0] in userlist.keys():
                    tmp['user1'] = userlist['uid_%s'%v[0]]
                else:
                    tmp['user1'] = []
                if v[1] and 'uid_%s'%v[1] in userlist.keys():
                    tmp['user2'] = userlist['uid_%s'%v[1]]
                else:
                    tmp['user2'] = []
                if v[2] and 'uid_%s'%v[2] in userlist.keys():
                    tmp['user3'] = userlist['uid_%s'%v[2]]
                else:
                    tmp['user3'] = []
                ret.append(tmp)

        #修改用户的邮箱
        for k,v in userlist.items():
            userinfo = User.query.filter(User.name == v[0]).first()
            if  userinfo:
                original_email = userinfo.email
                original_email_tmp_array = original_email.split(",")
                zeus_email = v[1]
                zeus_email_tmp_array = zeus_email.split(",")
                for item_email in zeus_email_tmp_array:
                    if item_email not in original_email_tmp_array:
                        original_email_tmp_array.append(item_email)
                userinfo.email = ",".join(original_email_tmp_array)
                db.session.commit()
                
        #默认关注主机  等晓帆他们的zabbix分支接入进来就好了，表叫什么哇
        for item in ret:
            host_info = Host.query.filter(and_(Host.hostname == item['hostname'],Host.deleted == 0)).first()
            if  host_info:
                host_id = host_info.id
                if item['user1']:
                    user_info = User.query.filter(User.name == item['user1'][0]).first()
                    if user_info:
                        hasIn = Alarm.query.filter(and_(Alarm.uid == user_info.id,Alarm.type == Alarm.TYPE_HOST,Alarm.target_id == host_id)).first()
                        if not hasIn:
                            target = Alarm(Alarm.TYPE_HOST,host_id,uid = user_info.id)
                            db.session.add(target)
                            db.session.commit()
                            
                if item['user2']:
                    user_info = User.query.filter(User.name == item['user2'][0]).first()
                    if user_info:
                        hasIn = Alarm.query.filter(and_(Alarm.uid == user_info.id,Alarm.type == Alarm.TYPE_HOST,Alarm.target_id == host_id)).first()
                        if not hasIn:
                            target = Alarm(Alarm.TYPE_HOST,host_id,uid = user_info.id)
                            db.session.add(target)
                            db.session.commit()

                if item['user3']:
                    user_info = User.query.filter(User.name == item['user3'][0]).first()
                    if user_info:
                        hasIn = Alarm.query.filter(and_(Alarm.uid == user_info.id,Alarm.type == Alarm.TYPE_HOST,Alarm.target_id == host_id)).first()
                        if not hasIn:
                            target = Alarm(Alarm.TYPE_HOST,host_id,uid = user_info.id)
                            db.session.add(target)
                            db.session.commit()


