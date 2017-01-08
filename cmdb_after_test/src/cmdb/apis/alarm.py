#-*- coding: UTF-8 -*-
from flask import Blueprint, request, make_response
from application import db
from models.alarm import Alarm
from models.user import User
from models.host import Host
from views.functions import responsejson, addalarm


apialarm = Blueprint('apialarm', __name__)

@apialarm.route("/", methods=['GET', 'POST'])
def index():
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    if request.method == 'POST':
        hostname = request.form['hostname']
        oauth_id = request.form['oauth_id']
        user = User.query.filter(User.oauth_id == oauth_id).first()
        host = Host.query.filter(Host.hostname == hostname).first()
        if not host:
            errcode = 1002
            statuscode = 403
            msg = "请提供主机名"
            response = make_response(responsejson(errcode, msg), statuscode)
            return response
        if not user:
            errcode = 1002
            statuscode = 403
            msg = "请提供主机负责人的oauth_id"
            response = make_response(responsejson(errcode, msg), statuscode)
            return response
        addalarm(user.id, Alarm.TYPE_HOST, host.id)
        response = make_response(responsejson(errcode, msg), statuscode)
        return response
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误，添加主机失败"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response