# -*- coding: utf-8 -*-
# vm_search 部署在后台vm_search.sh
# check_info 每天跑一次，部署在crontab

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")#加入默认的扫描路径

from sqlalchemy import *
from flask.ext.script import Manager
from application import app, db
from models.host_ip import HostIp
from models.vm import Vm
from models.host import Host
from models.ip_address import IpAddress
from models.alarm import Alarm
from models.follow import Follow
from views.host import _operation_log, _get_ip
from views.functions import _set_used_ip
from config import VM_DATABASE_URI
from xml.dom import minidom
from tasks import host_device_changed
import datetime
import time
import re
import json

manager = Manager(app)


@manager.command
def vm_search():
    now_time = datetime.datetime.now()
    print("==============start %s============="%now_time)
    vm_info = Vm.query.filter(Vm.status == Vm.STATUS_UNPROCESS).order_by(Vm.id).first()
    if not vm_info:
        print("没有任务 %s"%now_time)
        print("===============end %s=============="%now_time)
    else:
        callback_counter = 0
        while True:#如果无法,进行三次尝试,如果三次都不行,那么等明天的Job进行修复了
            vm_id = vm_info.vm_id
            engine = create_engine(VM_DATABASE_URI, encoding='utf-8', echo=False)
            connection = engine.connect()
            info = connection.execute("select * from vm_pool where oid = %s"%vm_id).fetchone()
            hostname = info['name']
            xml = info['body']
            xmldoc = minidom.parseString(xml)
            primary_ip_id = _get_primary_ipid(xmldoc)
            parent_name = _get_parent_name(xmldoc)
            parent_id = _get_host_id(parent_name)
            if hostname and primary_ip_id and parent_name:
                host = Host.query.filter(Host.hostname == hostname).first()
                if host:
                    if host.primary_ip_id != primary_ip_id:
                        _set_used_ip(host.primary_ip_id)
                        host.primary_ip_id = primary_ip_id
                        _set_used_ip(primary_ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host.id)
                    if host.parent_id != parent_id:
                        host.parent_id = parent_id
                    if host.note != vm_info.content:
                        host.note = vm_info.content
                    host.deleted = host.DELETED_NO
                    db.session.commit()
                    add_hostip(xmldoc, host.id)
                    vm_info.status = vm_info.STATUS_SUCCESS
                    db.session.commit()
                    log = json.dumps({'create': '创建一台主机(API)'}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                    _operation_log(host.id, 0, log)
                    host_device_changed.delay(host.id, 1, 1)
                    print("===============success %s=============="%now_time)
                else:
                    vm_info.status = vm_info.STATUS_NOTEXIST
                    db.session.commit()
                    print("===============notexist %s=============="%now_time)
                break
            else:
                callback_counter += 1
                if callback_counter < 4:
                    time.sleep(60)
                    continue

                vm_info.status = vm_info.STATUS_FAIL
                db.session.commit()
                print("===============fail %s=============="%now_time)
                break


@manager.command
def check_info():
    now_time = datetime.datetime.now()
    print("==============start %s============="%now_time)
    vm = Vm.query.order_by(Vm.id).all()
    engine = create_engine(VM_DATABASE_URI, encoding='utf-8', echo=False)
    connection = engine.connect()
    for item in vm:
        origin_info = connection.execute("select * from vm_pool where oid = %s"%item.vm_id).fetchone()
        if origin_info['state'] == 3:
            hostname = origin_info['name']
            xml = origin_info['body']
            xmldoc = minidom.parseString(xml)
            primary_ip_id = _get_primary_ipid(xmldoc)
            parent_name = _get_parent_name(xmldoc)
            parent_id = _get_host_id(parent_name)
            host = Host.query.filter(Host.id == item.host_id).first()
            if host:
                host.deleted = 0
                db.session.commit()
                if host.hostname != hostname:
                    origin = host.hostname
                    host.hostname = hostname
                    db.session.commit()
                    log = json.dumps({'create': '主机名由%s更改为%s'%(origin,hostname)}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                    _operation_log(host.id, 0, log)
                if int(host.primary_ip_id) != int(primary_ip_id):
                    _set_used_ip(host.primary_ip_id)
                    origin_id = host.primary_ip_id
                    origin = _get_ip(origin_id)
                    host.primary_ip_id = primary_ip_id
                    _set_used_ip(host.primary_ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host.id)
                    ip = _get_ip(host.primary_ip_id)
                    db.session.commit()
                    host_ip_info = HostIp.query.filter(and_(HostIp.host_id == host.id,HostIp.ip_address_id == origin_id)).first()
                    if host_ip_info:
                        host_ip_info.ip_address_id = host.primary_ip_id
                        db.session.commit()
                    else:
                        add_hostip(xmldoc, host.id)
                    log = json.dumps({'create': '主机ip由%s更改为%s'%(origin,ip)}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                    _operation_log(host.id, 0, log)
                template = xmldoc.getElementsByTagName('CONTEXT')
                nodes = template[0].childNodes
                net_preg = re.compile('^ETH(\d*)_IP')
                eth = {}
                for node in nodes:
                    tagname = node.nodeName
                    p = net_preg.match(tagname)
                    if p:
                        net_name_id = p.groups()[0]
                        eth[net_name_id] = node.childNodes[0].nodeValue
                        ip_address_id = _get_ip_id(eth[net_name_id])
                ip_all = HostIp.query.filter(HostIp.host_id == host.id).all()
                for items in ip_all:
                    if eth.has_key(str(items.net_name_id)):
                        origin_ip = _get_ip(items.ip_address_id)
                        if origin_ip != eth[str(items.net_name_id)]:
                            _set_used_ip(items.ip_address_id)
                            items.ip_address_id = _get_ip_id(eth[str(items.net_name_id)])
                            _set_used_ip(items.ip_address_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, host.id)
                            db.session.commit()
                            log = json.dumps({'create': '主机ip由%s更改为%s'%(origin_ip, eth[str(items.net_name_id)])}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                            _operation_log(host.id, 0, log)
                    else:
                        HostIp.query.filter(HostIp.id == items.id).delete()
                        hostiptarget = HostIp(host_id = items.host_id, net_name_id = net_name_id, ip_address_id = ip_address_id, type = 99, content = "")
                        db.session.add(hostiptarget)
                        db.session.commit()
                        delete_ip = _get_ip(items.ip_address_id)
                        add_ip = _get_ip(ip_address_id)
                        log = json.dumps({'create': '端口由eth%s更改为eth%s，主机ip由%s更改为%s'%(items.net_name_id, net_name_id, delete_ip, add_ip)}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                        _operation_log(host.id, 0, log)
                if int(host.parent_id) != int(parent_id):
                    origin = _get_hostname(host.parent_id)
                    host.parent_id = parent_id
                    hostname = _get_hostname(host.parent_id)
                    db.session.commit()
                    log = json.dumps({'create': '主机宿主机由%s更改为%s'%(origin, hostname)}, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                    _operation_log(host.id, 0, log)
                host_device_changed.delay(host.id, 1, 2)
            else:
                print("无此主机")
        elif origin_info['state'] == 6:
            delete_host = Host.query.filter(and_(Host.id == item.host_id, Host.deleted == 0)).first()
            if delete_host:
                delete_host.deleted = 1
                _set_used_ip(delete_host.primary_ip_id)
                db.session.commit()
                hostip_info = HostIp.query.filter(HostIp.host_id == delete_host.id).all()
                if hostip_info:
                    for item in hostip_info:
                        _set_used_ip(item.ip_address_id)
                        db.session.commit()
                    HostIp.query.filter(HostIp.host_id == delete_host.id).delete()
                    db.session.commit()
                alarm = Alarm.query.filter(and_(Alarm.target_id == delete_host.id, Alarm.type == Alarm.TYPE_HOST)).first()
                db.session.delete(alarm)
                follow = Follow.query.filter(and_(Follow.target_id == delete_host.id, Follow.type == Follow.TYPE_HOST)).first()
                db.session.delete(follow)
                print("===========delete %s========="%delete_host.hostname)
        else:
            pass
    print("===============end %s=============="%now_time)

def _get_hostname(id):
    host = Host.query.filter(Host.id == id).first()
    if host:
        return host.hostname
    return 0

def _get_primary_ipid(xmldoc):
    template = xmldoc.getElementsByTagName('CONTEXT')
    nodes = template[0].childNodes
    net_preg = re.compile('^ETH(\d*)_IP')
    for node in nodes:
        tagname = node.nodeName
        p = net_preg.match(tagname)
        if p:
            if p.groups()[0] == "0":
                primary_ip = node.childNodes[0].nodeValue
                primary_ip_id = _get_ip_id(primary_ip)
                return primary_ip_id

def _get_ip_id(ip):
    ip_info = IpAddress.query.filter(IpAddress.ipv4 == str(ip)).first()
    if ip_info:
        return ip_info.id
    return 0

def _get_parent_name(xmldoc):
    parent_names = xmldoc.getElementsByTagName('HOSTNAME')
    if len(parent_names) > 1:
        for item in parent_names:
            parent_name = item.firstChild.nodeValue
        return parent_name
    else:
        return

def _get_host_id(hostname):
    host_info = Host.query.filter(Host.hostname == hostname).first()
    if host_info:
        return str(host_info.id)

def add_hostip(xmldoc, host_id):
    template = xmldoc.getElementsByTagName('CONTEXT')
    nodes = template[0].childNodes
    net_preg = re.compile('^ETH(\d*)_IP')
    for node in nodes:
        tagname = node.nodeName
        p = net_preg.match(tagname)
        if p:
            net_name_id = p.groups()[0]
            ip = node.childNodes[0].nodeValue
            ip_address_id = _get_ip_id(ip)
            hasIn = HostIp.query.filter(and_(HostIp.host_id == host_id, HostIp.net_name_id == net_name_id, HostIp.ip_address_id == ip_address_id)).first()
            if not hasIn:
                hostiptarget = HostIp(host_id=host_id, net_name_id=net_name_id, ip_address_id=ip_address_id, type=99, content="")
                db.session.add(hostiptarget)
                db.session.commit()
                return
    return

if __name__ == "__main__":
    manager.run()
