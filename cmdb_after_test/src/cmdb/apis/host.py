#-*- coding: UTF-8 -*-
from flask import Blueprint, request, make_response
from sqlalchemy import *
from datetime import datetime
from application import app, db
from models.host import Host
from models.host_ip import HostIp
from models.ip_address import IpAddress
from models.vm import Vm
from models.device_ip import DeviceIp
from models.alarm import Alarm
from models.follow import Follow
from models.pool_host import PoolHost
from views.ip import find_ipv4,get_ipinfo
from views.device import _operation_log as device_operation_log
from views.host import _get_ip_id, _get_ip, _operation_log as __host_op_log, __add_net, __delete_net, __get_ip_info
from views.functions import _set_used_ip, responsejson, zabbix_rmhost, api_wrap_response,api_auth_check
from tasks import host_device_changed
from sqlalchemy import or_, and_
from config import VM_DATABASE_URI
import json

apihost = Blueprint('apihost', __name__)


@apihost.route("/", methods=['GET', 'POST'])
def add_host():
    if request.method == 'POST':
        if "vm_id" in request.form:
            return vm_add()
        else:
            parent_ip = ""
            parent_host_name = ""
            hostname = request.form['hostname']
            ip = request.form['ip']
            primary_ip_id = _get_ip_id(ip)
            is_virtual = int(request.form['is_virtual'])
            if "parent_host_name" in request.form:
                parent_host_name = request.form['parent_host_name']
            if "parent_ip" in request.form:
                parent_ip = request.form['parent_ip']
            parent_id = _get_parent_id(parent_host_name, parent_ip)
            response = add_virtual(hostname, primary_ip_id, is_virtual, parent_id)
            return response
    elif request.method == 'GET':
        return _get_hosts_info()
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误，添加主机失败"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response


def vm_add():
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    vm_id = request.form['vm_id'].strip()
    content = request.form['msg'].strip()
    hostname = request.form['hostname'].strip()
    if not hostname:
        engine = create_engine(VM_DATABASE_URI, encoding='utf-8', echo=True)
        connection = engine.connect()
        info = connection.execute("select * from vm_pool where oid = %s"%vm_id).fetchone()
        hostname = info['name']
    hasIn = Host.query.filter(Host.hostname == hostname).first()
    if hasIn:
        errcode = 1006
        statuscode = 400
        msg = "此主机已存在"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response
    hosttarget = Host(hostname=hostname, primary_ip_id=0, type=1, is_virtual=1, parent_id=0, device_id=0, status=2, cpu=0, memory=0, storage=0, note=content, deleted=1)
    db.session.add(hosttarget)
    db.session.commit()
    vmtarget = Vm(vm_id=vm_id, status=0, content=content, host_id=hosttarget.id)
    db.session.add(vmtarget)
    db.session.commit()
    response = make_response(responsejson(errcode, msg), statuscode)
    return response

def add_virtual(hostname, primary_ip_id, is_virtual, parent_id):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    if is_virtual == 1:
        if parent_id <= 0:
            errcode = 1002
            statuscode = 403
            msg = "请提供虚拟机所属宿主机"
            response = make_response(responsejson(errcode, msg), statuscode)
            return response
        else:
            hasIn = Host.query.filter(and_(Host.hostname == hostname, Host.primary_ip_id == primary_ip_id, Host.parent_id == parent_id)).all()
            if hasIn:
                errcode = 1006
                statuscode = 400
                msg = "此主机已存在"
                response = make_response(responsejson(errcode, msg), statuscode)
                return response
            hosttarget = Host(hostname=hostname, primary_ip_id=primary_ip_id, type=1, is_virtual=is_virtual, parent_id=parent_id, device_id=0, status=2, cpu=0, memory=0, storage=0)
            db.session.add(hosttarget)
            db.session.commit()
            host_device_changed.delay(hosttarget.id, 1, 1)
            _set_used_ip(primary_ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, hosttarget.id)
            log = json.dumps({'create': '创建一台主机(API)'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            __host_op_log(hosttarget.id, 0, log)
            response = make_response(responsejson(errcode, msg), statuscode)
            return response
    else:
        errcode = 1001
        statuscode = 400
        msg = "所选择主机不是虚拟机"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response

def _get_hosts_info(fr = 0):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    total = 0
    list = []

    ip_info = find_ipv4()
    device_list = DeviceIp.query.filter(DeviceIp.net_name_id == 0).all()
    device_info = {}
    if device_list:
        for device_item in device_list:
            if device_item.ip_address_id in ip_info:
                device_info[device_item.device_id] = ip_info[device_item.ip_address_id]
            else:
                tmp_ip_info = get_ipinfo(id = device_item.ip_address_id )
                if tmp_ip_info:
                    device_info[device_item.device_id] = tmp_ip_info.ipv4

    host_list = db.session.query(Host.hostname,Host.id,Host.device_id,HostIp.ip_address_id, HostIp.net_name_id,HostIp.type).outerjoin(HostIp,Host.id == HostIp.host_id).filter(Host.deleted == Host.DELETED_NO).all()
    host_info = {}
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

        for host_id,item_host in host_info.iteritems():
            tmp = {"hostname":item_host['hostname'], "ip":{}, "rc_ip":''}
            iplist = {}
            for item_ip in item_host['ipaddress']:
                if item_ip['type'] == 99:
                    net_name_label = 'eth' + str(item_ip['net_name_id'])
                    iplist[net_name_label] = ip_info[item_ip['ip_id']]
            tmp['ip'] = iplist
            if item_host['device_id'] and item_host['device_id'] in device_info.keys():
                tmp['rc_ip'] = device_info[item_host['device_id']]
            list.append(tmp)
    if fr == 1:
        return {
            'code':errcode,
            'msg':msg,
            'total':total,
            'list':list
        }
    else:
        response = make_response(responsejson_all(errcode, msg, total, list = list), statuscode)
        return response

@apihost.route("/<param>", methods=['PUT', 'POST', 'DELETE', 'GET'])
def modify_status(param):
    if param.strip().split(':'):
        tmp_arr = param.split(':')
        function_name = tmp_arr[0].strip()
        if function_name == "hostname":
            # tmp_arr[1]         = tmp_arr[1].strip().replace('web','').replace('kvm','').replace('hd','').replace('vm','').replace('db','')
            tmp_arr[1] = tmp_arr[1].strip()
            n = tmp_arr[1].index("tjtx")
            tmp_arr[1] = tmp_arr[1][n:]
            param = tmp_arr[0] + ':' + tmp_arr[1]
    else:
        errcode = 1004
        statuscode = 400
        msg = "输入格式不正确"
        response = make_response(responsejson(errcode,msg), statuscode)
        return response

    if request.method == 'POST' or request.method == 'PUT':
        host_info = _host_info(param)
        if host_info:
            return __modify_host(host_info)
        else:
            return not_exist()
    elif request.method == 'DELETE':
        return _delete_host(param)
    elif request.method == 'GET':
        return _get_host_info(param)
    else:
        errcode = 999
        statuscode = 405
        msg = "请求方法错误，修改主机状态失败"
        response = make_response(responsejson(errcode, msg), statuscode)
        return response


def __modify_host(host_info):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    try:
        random = request.form['random']
        access_token = request.form['access_token']
        check_ret = api_auth_check(random,access_token)
        if not check_ret:
            statuscode = 401
            msg = '未授权'
            return  api_wrap_response(errcode, msg, statuscode)
        if 'status' in request.form:
            status = request.form['status']
            host_info.status = status
            db.session.commit()
            host_device_changed.delay(host_info.id, 1, 2)
            log = json.dumps({'create': '机器status:从'+ str(status) + '更改为' + str(host_info.status) + '(API)'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            __host_op_log(host_info.id, 0, log)
        elif 'ip_change' in  request.form:#IP变更需求
                ip_delete_list = json.loads(request.form['ip_delete'])
                ip_add_list    = json.loads(request.form['ip_add'])
                if len(ip_delete_list) > 0:
                    for item in  ip_delete_list:
                        tmp_ip_address_info = __get_ip_info(item['ip'])
                        if not tmp_ip_address_info:
                            msg += '此IP(%s)不存在'%item['ip']
                            continue

                        tmp_ip_address_id = tmp_ip_address_info.id
                        tmp_net_name_id = item['net_name_id']
                        tmp_type = item['type']
                        ret = __delete_net(id = host_info.id,net_name_id = tmp_net_name_id ,ip_address_id = tmp_ip_address_id,type = tmp_type)
                        if ret:
                            log = json.dumps({'ip_delete': '删除IP: %s(API)'%item['ip']}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                            __host_op_log(host_info.id, 0, log)
                        else:
                             msg += '删除失败,此ip(%s)不是此主机的'%item['ip']

                if len(ip_add_list) > 0:
                    for item in  ip_add_list:
                        tmp_ip_address_info = __get_ip_info(item['ip'])
                        if not tmp_ip_address_info:
                            msg += '此IP(%s)不存在'%item['ip']
                            continue
                        if tmp_ip_address_info.flag == 0:
                            tmp_ip_address_id = tmp_ip_address_info.id
                            tmp_net_name_id = item['net_name_id']
                            tmp_type = item['type']
                            tmp_content = item['content']
                            tmp_primary = item['primary']
                            ret = __add_net(id = host_info.id,net_name_id = tmp_net_name_id ,ip_address_id = tmp_ip_address_id,type = tmp_type,content = tmp_content)
                            if ret:
                                log = json.dumps({'ip_add': '添加IP: %s(API)'%item['ip']}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                                __host_op_log(host_info.id, 0, log)
                            else:
                                msg += '此主机已经有此IP%s'%item['ip']
                        else:
                             msg += '此IP(%s)已经被占用'%item['ip']
    except  Exception,e:
        import traceback
        print traceback.format_exc()
        errcode = 999
        statuscode = 405
        msg = "请求方法错误:授权未通过或者ip_delete/ip_add必须json"
    return  api_wrap_response(errcode, msg, statuscode)


def _host_info(param):
    key,value = param.split(':')
    if key == "id":
        host_info = Host.query.filter(Host.id == int(value)).first()
    if key == "ip":
        ip_id = _get_ip_id(value)
        host_info = Host.query.filter(Host.primary_ip_id == ip_id).first()
    if key == "hostname":
        host_info = Host.query.filter(Host.hostname == value).first()
    return host_info

def _delete_host(param):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    host_info = _host_info(param)
    if host_info:
        from views.host import __delete_host
        if __delete_host(host_info):
            return make_response(responsejson(errcode, msg), statuscode)
        else:
            return not_exist()
    else:
        return not_exist()

def _get_host_info(param):
    errcode = 0
    statuscode = 200
    msg = "操作成功!"
    key,value = param.split(':')
    if key == "id":
        host_info = Host.query.filter(Host.id == int(value)).first()
        host_id = host_info.id
    if key == "hostname":
        host_info = Host.query.filter(Host.hostname == value).first()
        host_id = host_info.id
    if key == "ip":
        ip_id = _get_ip_id(value)
        host_info = HostIp.query.filter(HostIp.ip_address_id == ip_id).first()
        host_id = host_info.host_id
    if host_info:
        host_ip = HostIp.query.filter(HostIp.host_id == host_id).all()
        host_info = Host.query.filter(Host.id == host_id).first()
        iplist = {}
        viplist = {}
        for item in host_ip:
            if item.type == 99:
                net_name_label = 'eth' + str(item.net_name_id)
                iplist[net_name_label] = _get_ip(item.ip_address_id)
            else:
                net_name_label = 'eth' + str(item.net_name_id)
                if viplist.has_key(net_name_label):
                    viplist[net_name_label].append(_get_ip(item.ip_address_id))
                else:
                    viplist[net_name_label] = [_get_ip(item.ip_address_id)]
        #获取主机在哪些Pool
        pool_infos = PoolHost.query.filter(PoolHost.host_id == host_id).all()
        pool_ids = []
        if pool_infos:
            for pool_item in pool_infos:
                pool_ids.append(pool_item.pool_id)
        data = []
        data.append({"hostname":host_info.hostname,
                     "ip":iplist,
                     "vip":viplist,
                     "is_virtual":host_info.is_virtual,
                     "parent_id":host_info.parent_id,
                     "device_id":host_info.device_id,
                     "memory":host_info.memory,
                     "cpu":host_info.cpu,
                     "storage":host_info.storage,
                     "pool_ids":pool_ids
        })
        response = make_response(responsejson(errcode, msg, data=data), statuscode)
        return response
    else:
        return not_exist()

def not_exist():
    errcode = 1005
    statuscode = 400
    msg = "所选择主机不存在！"
    response = make_response(responsejson(errcode, msg), statuscode)
    return response

def _get_parent_id(parent_host_name, parent_ip):
    parent_ip_id = _get_ip_id(parent_ip)
    host_info = Host.query.filter(or_(Host.hostname == parent_host_name, Host.primary_ip_id == parent_ip_id)).all()
    for item in host_info:
        if item.primary_ip_id != 0:
            return item.id

class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

def responsejson_all(errcode, msg, total, list):
    return app.response_class(json.dumps({'errcode': errcode, 'msg': msg, 'total': total, 'list': list}, cls = CJsonEncoder), mimetype = 'application/json')