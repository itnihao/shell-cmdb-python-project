#-*- coding: UTF-8 -*-
from flask import Blueprint, request, make_response
from application import app
from models.alarm import Alarm
from models.user import User
from models.host import Host
from views.functions import responsejson, addalarm
import json
import urllib2


rmmonitor = Blueprint('rmmonitor', __name__)

@rmmonitor.route("/<param>", methods=['GET', 'POST'])
def index(param):
    if param.strip().split(':'):
        zabbix_name = param.split(':')[0].strip()
        hosts       = param.split(':')[1].strip()
        if zabbix_name == "zabbix10":
            return hostname(value)
    else:
        errcode = 1004
        statuscode = 400
        msg = "输入格式不正确"
        response = make_response(responsejson(errcode,msg), statuscode)
        return response
    url = "http://zabbix10.corp.anjuke.com/api_jsonrpc.php"
    header = {"Content-Type": "application/json"}
    data = json.dumps(
    {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
        "user": "admin",
        "password": "YWprX29wcwo="
    },
    "id": 0
    })
    auth_id =""
    request = urllib2.Request(url,data)
    for key in header:
        print header[key]
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)
    except urllib2.URLError as e:
        print "Auth Failed, Please Check Your Name And Password:",e.reason
    else:
        response = json.loads(result.read())
        result.close()
        print "zabbix auth_id is :", response['result']