# coding=utf-8
__author__ = 'qiqi'

from flask import Blueprint, request, make_response
from sqlalchemy import and_
from application import app, db
from models.host import Host
from models.device import Device
from models.device_ip import DeviceIp
from models.remote_card import RemoteCard
from views.functions import responsejson
import json

apiremotecard = Blueprint('apiremotecard', __name__)
#user api入口
#/api/cmdb/remotecard/hostname:xxx?random=1&access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
@apiremotecard.route("/<param>", methods=['GET', 'POST'])
def index(param):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    import hashlib
    random = request.args.get('random')
    access_token = request.args.get('access_token')
    check_token = hashlib.md5('%s%s'%('cmdb_api',random)).hexdigest()
    if check_token != access_token:
        statuscode = 401
        msg = '未授权'
        return make_response(responsejson(statuscode, msg), statuscode)

    if request.method == 'GET':
        if param.strip().split(':'):
            tmp_arr = param.split(':')
            function_name = tmp_arr[0].strip()
            if function_name == "hostname":
                tmp_arr[1] = tmp_arr[1].strip()
                n = tmp_arr[1].index("tjtx")
                hostname = tmp_arr[1][n:]
                try:
                    host = Host.query.filter(Host.hostname == hostname,Host.deleted == 0).first()
                    device = Device.query.filter(and_(Device.deleted == 0,Device.id == host.device_id)).first()
                    print device.id
                    deviceip = DeviceIp.query.filter(DeviceIp.device_id == device.id).first()
                    remotecard = RemoteCard.query.filter(RemoteCard.ip_id == deviceip.ip_address_id).first()
                except:
                    errcode = 1004
                    statuscode = 400
                    msg = "API出错！请联系管理员"
                    response = make_response(responsejson(errcode,msg), statuscode)
                    return response

                if remotecard:
                    statuscode = 200
                    a = app.response_class(json.dumps({'code':statuscode,'hostname':hostname,'deviceid':device.id,'remotecarduser':remotecard.user,'remotecardpass':remotecard.password}), mimetype = 'application/json')
                    response = make_response(a, statuscode)
                    return response
                else:
                    errcode = 1006
                    statuscode = 404
                    msg = "未找到该远控卡"
                    response = make_response(responsejson(errcode,msg), statuscode)
                    return response

        else:
            errcode = 1005
            statuscode = 400
            msg = "输入格式不正确"
            response = make_response(responsejson(errcode,msg), statuscode)
            return response
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response