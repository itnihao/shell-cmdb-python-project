# -*- coding: utf-8 -*-

from fabric.api import *
from application import db,app
from models.ip_address import IpAddress
from models.host_ip import HostIp
from models.host import Host
from views.functions import _set_used_ip
from sqlalchemy import and_
import re
import datetime

env.user = 'root'
env.abort_on_prompts = True
env.debug = True
env.password = 'anjukeansible'
env.key_filename = '/root/.ssh/ansible_rsa'
env.abort_exception = True
env.warn_only = True
env.time_out = 3
env.skip_bad_hosts = True


class RealCmdbIp:
    def run(self):
        time = datetime.datetime.now()
        output = open('/tmp/check_ip_fail.txt', 'a')
        output.write('=====time:%s=====\r\n'%time)
        output.close()
        print("===time:%s==="%time)
        host = self.get_hosts()
        message = []
        tmp_content_fail = ""
        tmp_content = ""
        for (k1,v1) in host.items():
            host_id = k1
            has = 0
            for item in v1['ip']:
                if "eth0" in item:
                    has = 1
                    env.host = item['eth0']
            try:
                cmd = execute(self.check_ip, host=env.host)
            except:
                tmp_content_fail += self.faillog(6,host_id,env.host,'Needed to prompt for a connection or sudo password')+"<br/>"
                continue
            if cmd:
                if 'Timed out' in str(cmd[env.host]):
                    tmp_content_fail += self.faillog(1,host_id,env.host,cmd[env.host])+"<br/>"
                elif 'No route to host' in str(cmd[env.host]):
                    tmp_content_fail += self.faillog(4,host_id,env.host,cmd[env.host])+"<br/>"
                elif 'Connection refused' in str(cmd[env.host]):
                    tmp_content_fail += self.faillog(5,host_id,env.host,cmd[env.host])+"<br/>"
                elif 'Underlying exception' not in str(cmd[env.host]):
                    ifconfig = cmd[env.host]
                    all_ips = re.findall(r'^(\S+).*?inet addr:(\S+).*?Mask:(\S+)', ifconfig, re.S | re.M)
                    print("===以机器上ip为基准===")
                    for host_ip in all_ips: #所抓ip一个一个循环
                        real_ip = {host_ip[0]:host_ip[1]}
                        if "eth" in host_ip[0]:
                            if real_ip in v1['ip']:
                                continue
                            else:
                                print("cmdb少: %s"%real_ip)
                                tmp_content += "主机ID:%s，hostname:%s，cmdb少: %s<br/>"%(k1,v1['hostname'],real_ip)
                        else:
                            if real_ip == {'lo':'127.0.0.1'}:
                                pass
                            else:
                                print("cmdb少: %s"%real_ip)
                                tmp_content += "主机ID:%s，hostname:%s，cmdb少: %s:%s<br/>"%(k1,v1['hostname'],host_ip[0],host_ip[1])

                    print("===以cmdb中ip为基准===")
                    real = []
                    for host_ip in all_ips:
                        real_ip = {host_ip[0]:host_ip[1]}
                        real.append(real_ip)
                    for item in v1['ip']:
                        if item in real:
                            continue
                        else:
                            print("cmdb多: %s"%item)
                            tmp_content += "主机ID:%s，hostname:%s，cmdb多: %s<br/>"%(k1,v1['hostname'],item)
            else:
                tmp_content_fail += self.faillog(2,host_id,env.host,cmd[env.host])+"<br/>"

            if has == 0:      #cmdb里没有eth0，无法远程登录
                print("host_id:%s 没有eth0"%k1)
                tmp_content += "主机ID:%s，hostname:%s，没有eth0"%(k1,v1['hostname'])+"<br/>"
        message.append(tmp_content_fail)
        message.append(tmp_content)
        print '---------开始发邮件-------------'
        from views.functions import addmail
        subject = "[主机IP核对]%s核对结果"%datetime.datetime.now().strftime("%Y-%m-%d")
        content = "<br/><br/>".join(message)
        receiver = app.config.get("MAIL_TO")['check_cmdb_ip']
        print receiver
        print content
        content = "<style type='text/css'>body{fonts-size:18px;}</style>"+content
        addmail(receiver, subject, content)
        print('-------邮件发送结束------')

    def get_hosts(self):
        hostname = {}
        host_ids = []
        host_info = Host.query.filter(Host.deleted == 0).all()
        for item in host_info:
            host_ids.append(item.id)
            hostname[item.id] = item.hostname
        hostip_info = HostIp.query.filter(HostIp.host_id.in_(host_ids)).order_by(HostIp.host_id).all()
        host = {}
        iplist = {'ip':[],'hostname':""}
        tmphostid = 0
        for item in hostip_info:
            #print(item.host_id)
            if tmphostid != item.host_id:
                iplist = {'ip':[],'hostname':""}
            tmplist = {}
            if item.type == 99:
                net_name_label = 'eth' + str(item.net_name_id)
                tmplist[net_name_label] = self._get_ip(item.ip_address_id)
            else:
                net_name_label = 'eth' + str(item.net_name_id) + ":" + str(item.type)
                tmplist[net_name_label] = self._get_ip(item.ip_address_id)
            iplist['ip'].append(tmplist)
            iplist['hostname'] = hostname[item.host_id]
            host[item.host_id] = iplist
            tmphostid = item.host_id
        return host

    def _get_ip(self,ip_id):
        ip_info = IpAddress.query.filter(IpAddress.id == ip_id).first()
        return ip_info.ipv4

    def _get_ip_id(self,ip):
        ip_info = IpAddress.query.filter(IpAddress.ipv4 == ip).first()
        return ip_info.id

    def check_ip(self):
        a = run('ifconfig')
        return a

    def change_ip(self,old_ip,new_ip,host_id):
        old_ip_id = self._get_ip_id(old_ip)
        new_ip_id = self._get_ip_id(new_ip)
        target = HostIp.query.filter(and_(HostIp.host_id == int(host_id),HostIp.ip_address_id == old_ip_id)).first()
        target.ip_address_id = new_ip_id
        _set_used_ip(old_ip_id)
        _set_used_ip(new_ip_id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, int(host_id))
        db.session.commit()

    def del_ip(self,k2,v2,host_id):
        print("====del_ip====")
        ip = k2.split(":")
        if len(ip) == 1:
            type = 99
        else:
            type = int(ip[1])
        net_name_id = int(ip[0][-1])
        target = HostIp.query.filter(and_(HostIp.host_id == host_id,HostIp.type == type,HostIp.net_name_id == net_name_id)).first()
        if target:
            db.session.delete(target)
            db.session.commit()
            print("host_id:%s cmdb中多一个ip:%s:%s，已删除"%(host_id,k2,v2))

    def add_ip(self,eth,ip,host_id):
        print("====add_ip====")
        net = eth.split(":")
        ip_id = self._get_ip_id(ip)
        if len(net) == 1:
            type = 99
        else:
            type = int(net[1])
        net_name_id = int(net[0][-1])
        target = HostIp(host_id,net_name_id,ip_id,type)
        db.session.add(target)
        db.session.commit()
        print("host_id:%s cmdb中缺少ip:%s:%s，已添加"%(host_id,eth,ip))

    def faillog(self,type,hostname,ip,msg):
        output = open('/tmp/check_ip_fail.txt', 'a')
        try:
            output.write('fail[type:%s]:HOST_ID:%s,IP:%s,MSG:%s\r\n'%(type,hostname,ip,msg))
            content = 'fail[type:%s]:HOST_ID:%s,IP:%s,MSG:%s\r\n'%(type,hostname,ip,msg)
        finally:
            output.close()
        return content
