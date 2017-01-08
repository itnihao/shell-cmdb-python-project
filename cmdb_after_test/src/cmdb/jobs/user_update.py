# -*- coding: utf-8 -*-
'''
  此job用来去除已离职人员订阅的报警以及关注的主机和poll
  每个星期跑一次
'''

from application import app, db
from models.user import User
from models.alarm import Alarm
from models.follow import Follow
from views.user import unalarm,unfollow,insert_user_info,init_user_role
from views.functions import  oa_interface
import hashlib
import urllib,urllib2
import datetime
import json

class User_Update:
    def run(self):
        print "=======start========"
        self.get_shuser_info()
        self.update_user_status()
        print "=======end========="

    def get_shuser_info(self):
        shuser_info = self.get_all_info()
        if shuser_info['status'] == 1:
            user_info = shuser_info['data']
            for item in user_info:
                cmdb_user_info = User.query.filter(User.name == item['domain_account']).first()
                if not cmdb_user_info:
                    insert_user_info('',item,0)
                    init_user_role(item['user_id'])

    def update_user_status(self):
        user_list = User.query.all()
        if user_list:
            for user_item in user_list:
                oa_info = oa_interface(user_item.name,superior=1)
                if oa_info['status'] == 1:
                    job_status = int(oa_info['data']['job_status'])
                    if job_status == 1:
                        user_item.p_level = int(oa_info['data']['p_level'])
                        user_item.m_level = int(oa_info['data']['m_level'])
                        user_item.department_id = int(oa_info['data']['department_id'])
                        user_item.department_name = oa_info['data']['department_name']
                        user_item.function_id = oa_info['data']['function_id']
                        user_item.function_name = oa_info['data']['function_name']
                        superior_id = 0
                        if oa_info['data']['superior']:
                            name = oa_info['data']['superior']['domain_account']
                            user_info = User.query.filter(User.name == name).first()
                            if user_info:
                                superior_id = user_info.id
                        user_item.superior_id = superior_id
                        if user_item.status == 1:
                            user_item.status = 0
                        db.session.commit()
                    else:
                        user_item.status = 1
                        db.session.commit()
                        user_id = user_item.id
                        self.remove_alarm(user_id)
                        self.remove_follow(user_id)

    def remove_alarm(self,user_id,pooid=0,hostid=0):
        if pooid !=0 or hostid !=0:
            if pooid:
                unalarm(user_id,1,pooid)
            if hostid:
                unalarm(user_id,2,hostid)
        else:
            user_alarm = Alarm.query.filter(Alarm.uid == user_id).all()
            if user_alarm:
                for info in user_alarm:
                    unalarm(info.uid,info.type,info.target_id)

    def remove_follow(self,user_id,pooid=0,hostid=0):
        if pooid !=0 or hostid !=0:
            if pooid:
                unfollow(user_id,1,pooid)
            if hostid:
                unfollow(user_id,2,hostid)
        user_follow = Follow.query.filter(Follow.uid == user_id).all()
        if user_follow:
            for info in user_follow:
                unfollow(info.uid,info.type,info.target_id)

    #按照域城市id获取信息到OA取数据
    def get_all_info(self):
        params = {
            'city_id':11
        }
        sort_keys = sorted(params)
        params_str = ""
        for item_key in sort_keys:
            params_str += "%s=%s&"%(item_key,params[item_key])
        params_str = params_str[0:-1]
        params_str += "ajkzwww"
        params['auth'] = hashlib.md5(params_str.encode('utf-8')).hexdigest()
        data = urllib.urlencode(params)
        req = urllib2.Request(" http://home.corp.anjuke.com/api/getUsers/",data)
        response = urllib2.urlopen(req)
        info = response.read()
        oa_userinfo = {}
        if info:
            oa_userinfo = json.loads(info)
        return oa_userinfo