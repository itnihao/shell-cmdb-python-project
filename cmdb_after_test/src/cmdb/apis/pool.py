#-*- coding: UTF-8 -*-
from flask import Blueprint, request, make_response
from application import db
from models.pool import Pool
from models.host import Host
from models.pool_host import PoolHost
from models.device_ip import DeviceIp
from models.host_ip import HostIp
from views.functions import responsejson
from views.user import find_username,get_user_info
from views.ip import find_ipv4
from views.pool import find_userids
from apis.host import responsejson_all
from sqlalchemy import and_

apipool= Blueprint('apipool', __name__)

@apipool.route("/", methods=['GET', 'POST'])
def index():
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
        total = 0
        list = []
        pool_info = Pool.query.all()
        owner_ids=find_userids(pool_info)
        userlist = find_username(owner_ids)
        for item in pool_info:
            tmp = {"pool_id":item.id, "pool_name":item.source_desc+item.name,"ops_owner":userlist[item.ops_owner],"biz_owner":userlist[item.biz_owner],"team_owner":userlist[item.team_owner]}
            list.append(tmp)
        response = make_response(responsejson_all(errcode, msg, total, list=list), statuscode)
        return response
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response

@apipool.route("/<param>", methods=['GET', 'POST'])
def get_pool(param):
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
        key,value = param.split(':')
        hostids = []
        pool_info = Pool.query.filter(Pool.id == int(value)).first()
        if pool_info:
            pool_host = PoolHost.query.filter(PoolHost.pool_id == pool_info.id).all()
            if pool_host:
                for item in pool_host:
                    hostids.append(item.host_id)
            owner_ids = [pool_info.team_owner,pool_info.biz_owner,pool_info.ops_owner]
            #userlist = find_username(owner_ids)
            userlist = get_user_info(uids = owner_ids)
            ip_info = find_ipv4()
            device_list = DeviceIp.query.filter(DeviceIp.net_name_id == 0).all()
            device_info = {}
            if device_list:
                for device_item in device_list:
                    device_info[device_item.device_id] = ip_info[device_item.ip_address_id]
            host_list = db.session.query(Host.hostname,Host.id,Host.device_id,HostIp.ip_address_id, HostIp.net_name_id,HostIp.type).filter(Host.id.in_(hostids)).outerjoin(HostIp,and_(Host.deleted == Host.DELETED_NO,HostIp.host_id == Host.id )).all()
            host_info = {}
            total = 0
            data = {}
            host_ip = []
            if host_list:
                for item_host in host_list:
                    tmp_ipaddess = {'ip_id':item_host.ip_address_id,'net_name_id':item_host.net_name_id,'type':item_host.type}
                    if item_host.id in host_info.keys():
                        host_info[item_host.id]['ipaddress'].append(tmp_ipaddess)
                    else:
                        total += 1
                        tmp = {}
                        tmp['id'] = item_host.id
                        tmp['hostname'] = item_host.hostname
                        tmp['device_id'] = item_host.device_id
                        tmp['ipaddress'] = []
                        tmp['ipaddress'].append(tmp_ipaddess)
                        host_info[item_host.id] = tmp
                tmp = {}
                for host_id,item_host in host_info.iteritems():
                    tmp['hostname_ip'] = {"hostname":item_host['hostname'], "ip":{}, "rc_ip":''}
                    iplist = {}
                    for item_ip in item_host['ipaddress']:
                        if item_ip['type'] == 99:
                            net_name_label = 'eth' + str(item_ip['net_name_id'])
                            iplist[net_name_label] = ip_info[item_ip['ip_id']]
                    tmp['hostname_ip']['ip'] = iplist
                    if item_host['device_id'] and item_host['device_id'] in device_info.keys():
                        tmp['hostname_ip']['rc_ip'] = device_info[item_host['device_id']]
                    host_ip.append(tmp['hostname_ip'])
                data['hostname_ip'] = host_ip
                data['pool_name'] = pool_info.name
                data['team_owner'] = {"cn_name":userlist[pool_info.team_owner].cn_name, "email":userlist[pool_info.team_owner].email}
                data['biz_owner'] = {"cn_name":userlist[pool_info.biz_owner].cn_name, "email":userlist[pool_info.biz_owner].email}
                data['ops_owner'] = {"cn_name":userlist[pool_info.ops_owner].cn_name, "email":userlist[pool_info.ops_owner].email}
            response = make_response(responsejson(errcode, msg, data=data), statuscode)
            return response
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response