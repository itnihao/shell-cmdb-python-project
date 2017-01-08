#-*- coding: UTF-8 -*-
from flask import Blueprint, render_template

apipublic = Blueprint('apipublic', __name__)


@apipublic.route("/")
def index():
    apis = []
    apis.append({'name':'主机列表','url':'http://ops.corp.anjuke.com/api/cmdb/host'})
    apis.append({'name':'主机详情','url':'http://ops.corp.anjuke.com/api/cmdb/host/hostname:tjtx-102-230'})
    apis.append({'name':'接警主机的用户','url':'http://ops.corp.anjuke.com/api/user/hostname:tjtx-102-230'})
    apis.append({'name':'POOL列表','url':'http://ops.corp.anjuke.com/api/cmdb/pool?random=1&access_token=2658243290a3858c332fac195766c4bc'})
    apis.append({'name':'POOL详情','url':'http://ops.corp.anjuke.com/api/cmdb/pool/pool_id:147?random=1&access_token=2658243290a3858c332fac195766c4bc'})
    apis.append({'name':'远控卡信息','url':'http://ops.corp.anjuke.com/api/cmdb/remotecard/hostname:tjtx-98-224?random=1&access_token=2658243290a3858c332fac195766c4bc'})

    return render_template("apis/index.html",apis=apis)
