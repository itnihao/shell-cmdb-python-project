#-*- coding: UTF-8 -*-
from flask import Blueprint, request, make_response
from sqlalchemy import and_
from application import app, db
from models.user import User
from models.alarm import Alarm
from models.host import Host
from models.pool import Pool
from models.pool_host import PoolHost
from views.functions import responsejson, api_auth_check
import json
import re

apiuser = Blueprint('apiuser', __name__)
#签名验证
#参数 random:加密随机数
#参数 access_token=md5(key+random)
#user api入口
#/api/user/hostname:xxx
#/api/user/update
@apiuser.route("/<param>", methods=['GET', 'POST'])
def index(param):
    if param.strip().split(':'):
        tmp_arr = param.split(':')
        function_name = tmp_arr[0].strip()
        if function_name == "hostname":
            tmp_arr[1] = tmp_arr[1].strip()
            n = tmp_arr[1].index("tjtx")
            value = tmp_arr[1][n:]
            return search(value)
        elif function_name == "update":
            return update()
    else:
        errcode = 1004
        statuscode = 400
        msg = "输入格式不正确"
        response = make_response(responsejson(errcode,msg), statuscode)
        return response


def search(name):
    hostinfo = Host.query.filter(Host.hostname == name).first()
    if hostinfo:
        alarminfo = Alarm.query.filter(and_(Alarm.target_id == hostinfo.id,Alarm.type == 2)).all()
        host_uids = []
        if alarminfo:
            for item in alarminfo:
                host_uids.append(item.uid)
        pools = PoolHost.query.filter(PoolHost.host_id == hostinfo.id).all()
        info = []
        if pools:
            for item in pools:
                alarminfos  = Alarm.query.filter(and_(Alarm.target_id == item.pool_id,Alarm.type == 1)).all()
                if alarminfos:
                    for alarm in alarminfos:
                        info.append(alarm.uid)
        uids = list(set(host_uids).union(set(info)))
        maillist =""
        if len(uids):
            for user_id in uids:
                if user_id !=0:
                    userinfo = User.query.filter(and_(User.id == user_id,User.status ==0)).first()
                    if userinfo:
                        if len(maillist):
                            maillist = maillist + ',' + userinfo.email
                        else:
                            maillist = userinfo.email
        errcode = 0
        hostid = hostinfo.id
        hostname = hostinfo.hostname
        hosttype=hostinfo.type_descri
        statuscode = 200
        data = maillist
        response = make_response(xiepeng_responsejson(errcode,data,hostid,hostname,hosttype), statuscode)
        return response
    else:
        errcode = 1001
        statuscode = 404
        msg = "资源不存在"
        response = make_response(responsejson(errcode,msg), statuscode)
        return response

#方法只能POST
#参数 domain_name : 域账号,必需
#参数 status : 在职与否  0:在职   1:离职
def update():
    errcode = 0
    msg = 'success'
    if request.method == 'GET':
        statuscode = 405
        msg = '使用不允许的方法'
        return make_response(responsejson(statuscode, msg), statuscode)

    random = request.form['random']
    access_token = request.form['access_token']
    check_ret = api_auth_check(random,access_token)
    if not check_ret:
        statuscode = 401
        msg = '未授权'
        return make_response(responsejson(statuscode, msg), statuscode)

    domain_name = request.form['domain_name']
    userinfo = User.query.filter(User.name == domain_name).first()
    if not userinfo:
        statuscode = 404
        msg = '所请求资源不存在'
        return make_response(responsejson(statuscode, msg), statuscode)

    if 'status' in request.form:
        userinfo.status = request.form['status']

    db.session.commit()


def xiepeng_responsejson(errcode,msg,hostid=0,hostname="",hosttype=''):
    return app.response_class(json.dumps({'errcode': errcode,'msg': msg,'hostid':hostid,'hostname':hostname,'hosttype':hosttype}), mimetype = 'application/json')
