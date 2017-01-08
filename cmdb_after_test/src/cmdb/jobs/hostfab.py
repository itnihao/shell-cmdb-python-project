# -*- coding: utf-8 -*-
import json, time, re
from sqlalchemy import and_
from fabric.api import *
from application import app, db
from models.host import Host
from models.host_ip import HostIp
from models.ip_address import IpAddress
from models.device_ip import DeviceIp
from views.pool import get_ansible_passwd
from views.host import _operation_log,_get_ip
from tasks import host_device_changed


env.user = 'root'
#env.password = '%s'%get_ansible_passwd().strip()
env.password = 'anjukeansible'
env.key_filename = '/root/.ssh/ansible_rsa'
env.warn_only = True
env.time_out = 3
env.skip_bad_hosts = True
env.abort_on_prompts = True
env.abort_exception = True
env.disable_known_hosts = True

def abort(msg):
    print "================"
    print msg

class HostFab:
    def run(self):
        self.rc_flag = 0
        self.fail_hostids = []
        self.messages = {
            'fail':[],
            'compare':[],
            'rc':[]
        }
        self.info()
        ###发送邮件
        print('-------邮件发送开始------')
        from views.functions import addmail
        from flask import render_template
        subject = "[主机核对]"
        head = ['主机ID','主机名称','描述']
        bodys = []
        if len(self.messages['compare']) > 0 :
            for item in self.messages['compare']:
                if len(item['tips'])>0:
                    tmp_link_id = '<a href="http://ops.corp.anjuke.com/cmdb/host/%s">%s</a>'%(item['id'],item['id'])
                    tmp_link_hostname = '<a href="http://ops.corp.anjuke.com/cmdb/host/%s">%s</a>'%(item['id'],item['hostname'])
                    tmp_body=[tmp_link_id,tmp_link_hostname,",".join(item['tips'])]
                    bodys.append(tmp_body)
        avghead = ['主机ID','主机名称','失败描述']
        avgbodys = []
        if len(self.messages['fail']) > 0 :
            for item in self.messages['fail']:
                if len(item['tips'])>0:
                    tmp_link_id = '<a href="http://ops.corp.anjuke.com/cmdb/host/%s">%s</a>'%(item['id'],item['id'])
                    tmp_link_hostname = '<a href="http://ops.corp.anjuke.com/cmdb/host/%s">%s</a>'%(item['id'],item['hostname'])
                    tmp_body=[tmp_link_id,tmp_link_hostname,",".join(item['tips'])]
                    avgbodys.append(tmp_body)
        if len(bodys)>0:
            content = render_template('jobs/ratio.html',head = head,bodys = bodys,avghead = avghead,avgbodys = avgbodys)
            addmail(app.config.get("MAIL_TO")['ops_email'], subject, content)
        rc_head = ['主机名','CMDB远控卡','Job远控卡','描述']
        rc_bodys = []
        if self.messages['rc']:
            for item in self.messages['rc']:
                if len(item['tips'])>0:
                    tmp_link_hostname = '<a href="http://ops.corp.anjuke.com/cmdb/host/%s">%s</a>'%(item['id'],item['hostname'])
                    tmp_body=[tmp_link_hostname,item['pri_ip'],item['job_ip'],",".join(item['tips'])]
                    rc_bodys.append(tmp_body)
        if len(rc_bodys)>0:
            content = render_template('jobs/ratio.html',head = rc_head,bodys = rc_bodys,avghead = avghead,avgbodys = avgbodys)
            addmail(app.config.get("MAIL_TO")['ops_email'], subject, content)
        print('-------邮件发送结束------')

    def info(self):
        hosts = self.get_hosts()
        idx = 0
        if len(hosts) <= 0 :
            return 'over'

        for host in hosts:
            try:
                if idx<0:
                    break
                time.sleep(0.5)
                print '------ID:%s,Hostname:%s--------'%(host.id,host.hostname)
                if host.pri_ip:
                    if self.rc_flag == 1:
                        if host.is_virtual == 0:
                            self.run_ipmitool(host)
                    else:
                        self.run_hard(host)
                        if host.id in self.fail_hostids:
                            continue
                        self.run_ifconfig(host)
                else:
                    self.faillog(3,host.id,host.hostname,faillog,'No ip')
            except Exception as e:
                print "Error:%s"%e
            idx += 1

    def get_hosts(self):
        host_ids = []
        host_ips = {}
        all_hosts = []
        black_hostnams=["Mq10-002","ofe20-001","db20-005","ocn20-002","cdn20-006","cdn20-007","app20-002","app10-005","app10-004","app10-103","app10-065","app10-006","vm01-001","app10-037","vm20-002","app00-001","Dw00-001","app02-001","TEST-APP","192.168.201.63","192.168.201.56","192.168.1.7","BAK00-001","zabbix10-001","login10-005","TEST-APP","192.168.201.63","192.168.201.56","192.168.1.7","BAK00-001","lb00-001","lb00-002","bi20-003","app10-120","db20-043","apcbak20-001","apcbak20-004","test10-001","opsbak10-006","login10-002","xapp20-021","xapp10-065",
                        "xapp10-049","xapp10-048","xapp10-029","xapp10-027","xapp10-025","xapp10-023","xapp10-007","xapp10-047","xapp10-038","xapp20-024","xapp20-020","puppet10-002","xapp10-002","xapp10-080","xapp10-072",
                        "xapp10-071","xapp10-079","mon10-002","xapp20-030","xapp10-062","xapp10-039","xapp10-035","xapp10-033","xapp10-032","xapp10-031","xmq10-002","xlog10-002","xapp10-063","xapp10-036","xapp10-030","xapp10-028",
                        "xapp10-026","xapp10-050","xapp20-026","ajk_login","db10-154","xapp10-020","mon10-001","proxy10-001","cacti-syslog10","xapp10-058","xapp10-061","xqa10-001","xqa10-003","xapp10-073","xapp10-075",
                        "puppetmaster","xapp10-003","xapp10-005","xapp10-006","xapp10-016","xapp10-020","xapp10-053","xapp10-054","xapp10-069","xapp10-077","xapp10-078","xapp10-004","xapp10-008","xapp10-017","xapp10-022",
                        "xapp10-040","xapp20-032","xapp20-031","xapp20-022","xapp20-023","win_remote-control","win2003-sql","win2003_64-vcenter","windows2003-32-ita","xapp10-082","xqa20-001","xqa20-002","xmq10-001","xmq10-003","xmq10-004"]
        host_info = Host.query.filter(and_(Host.deleted == Host.DELETED_NO,Host.id>0)).order_by(Host.id.desc()).all()
        for item in host_info:
            if self.rc_flag == 1:
                if item.id in [21,25,30,32,50,57,59,63,65,66,68,69,70,71,76,77,78,81,205,206,222]:
                    continue
                if 'db' not in item.hostname.lower():
                    continue
            else:
                if item.hostname in black_hostnams:
                    continue

            all_hosts.append(item)
            host_ids.append(item.id)
        hostip_info = HostIp.query.filter(HostIp.host_id.in_(host_ids)).order_by(HostIp.host_id).all()

        for item in hostip_info:
            tmp_key  = 'host_%s'%item.host_id
            if tmp_key not in host_ips.keys():
                host_ips[tmp_key] = {'ips':[],'pri_ip':False}

            tmplist = {}
            if item.type == 99:
                net_name_label = 'eth' + str(item.net_name_id)
                tmplist[net_name_label] = _get_ip(item.ip_address_id)
            else:
                net_name_label = 'eth' + str(item.net_name_id) + ":" + str(item.type)
                tmplist[net_name_label] = _get_ip(item.ip_address_id)
            host_ips[tmp_key]['ips'].append(tmplist)

        for item in all_hosts:
            tmp_key  = 'host_%s'%item.id
            if tmp_key in host_ips.keys():
                item.ips = host_ips[tmp_key]['ips']
                item.pri_ip = _get_ip(item.primary_ip_id)
            else:
                item.ips = []
                item.pri_ip = False
        return all_hosts

    def run_hard(self,host):
        env.host = '%s'%host.pri_ip
        host_info = self.wrap_run(self.fabric_hard,host)
        if host_info:
            cpu=host_info[env.host][0]
            memory=host_info[env.host][1]
            storage=host_info[env.host][2]
            log_data={}
            if host.cpu != cpu:
                 log_data['cpu']="cpu从 %sCore 更改为 %sCore"%(host.cpu,cpu)
                 host.cpu = cpu
            if host.memory != memory:
                 log_data['memory']="memory %sG 更改为 %sG"%(host.memory,memory)
                 host.memory = memory
            if host.storage != storage:
                 src_storage = int(host.storage)
                 if src_storage == 0:
                    src_storage = '未知'
                 else:
                    if src_storage >= 1000:
                        src_storage = '%sT'% str(int(src_storage/1000))
                    else:
                        src_storage = '%sG'%str(src_storage)

                 des_storage = int(storage)
                 if des_storage == 0:
                    des_storage = '未知'
                 else:
                    if des_storage >= 1000:
                        des_storage = '%sT'% str(int(des_storage/1000))
                    else:
                        des_storage = '%sG'%str(des_storage)

                 log_data['storage']="storage %s 更改为 %s"%(src_storage,des_storage)

                 host.storage = storage
            if log_data:
                log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                _operation_log(host.id, 0, log)
            host_device_changed.delay(host.id, 1, 1)
            db.session.add(host)
            db.session.commit()

    def run_ifconfig(self,host):
        msglog = {
            'id':host.id,
            'hostname':host.hostname,
            'tips':[]
        }
        env.host = '%s'%host.pri_ip
        cmd = self.wrap_run(self.fabric_ifconfig, host)
        if cmd:
            ifconfig_text = str(cmd[env.host])
            ifconfig_text = ifconfig_text.split('\r\n\r\n')
            all_ips = []
            for item in ifconfig_text:
                ip = re.findall(r'^([a-z]+[\d:]{0,3}).*?inet addr:(\S+).*?',item,re.S | re.M)
                if ip:
                    all_ips.append(ip[0])

            #以机器上ip为基准
            for host_ip in all_ips: #所抓ip一个一个循环
                tmp_real_name = host_ip[0]
                tmp_real_name = tmp_real_name.replace("em","eth")
                tmp_real_ip = host_ip[1]
                tmp_real_json = {tmp_real_name:tmp_real_ip}
                if re.match(r'(\d)*\.(\d)*\.(\d)*\.(\d)*',tmp_real_ip):
                    if tmp_real_json in host.ips:
                        continue
                    else:
                        if tmp_real_ip in ['127.0.0.1']:
                            continue
                        if tmp_real_name in ['docker0','virbr0']:
                            continue
                        msglog['tips'].append('CMDB少 名称:%s,IP:%s<br/>'%(tmp_real_name,tmp_real_ip))
                else:
                    pass

           #===以cmdb中ip为基准===
            real_ips = []
            for host_ip in all_ips:
                tmp_real_name = str(host_ip[0])
                tmp_real_name = tmp_real_name.replace("em","eth")
                tmp_real_json = {tmp_real_name:host_ip[1]}
                real_ips.append(tmp_real_json)
            for item in host.ips:
                if item in real_ips:
                    continue
                else:
                    for tmp_real_name,real_ip in item.items():
                        msglog['tips'].append('CMDB多 名称:%s,IP:%s<br/>'%(tmp_real_name,real_ip))

        self.messages['compare'].append(msglog)


    def run_ipmitool(self,host):
        msglog = {
            'id':host.id,
            'hostname':host.hostname,
            'pri_ip':'',
            'job_ip':'',
            'tips':["<fonts color='%s'>%s</fonts>"%('red','不相等')]
        }
        env.host = '%s'%host.pri_ip
        cmd = self.wrap_run(self.fabric_ipmitool, host)
        if cmd:
            ipmitool = str(cmd[env.host])
            rc_ip = re.findall(r'IP\s*Address\s*:\s*(10\.[1-2]{1}0\.\d+\.\d+)\r\n',ipmitool,re.S | re.M)
            rc_ip = "".join(rc_ip)
            msglog['job_ip'] = rc_ip
            device_info = DeviceIp.query.filter(and_(DeviceIp.device_id == host.device_id,DeviceIp.net_name_id == 0)).first()
            if device_info:
                pri_ip =  _get_ip(device_info.ip_address_id)
                msglog['pri_ip'] = pri_ip
                if str(pri_ip) == str(rc_ip):
                    msglog['tips'][0] = "<fonts color='%s'>%s</fonts>"%('green','相等')

        self.messages['rc'].append(msglog)

    def wrap_run(self,run_func,host):
        ret = False
        try:
           ret = execute(run_func, host=env.host)
        except:
           return self.faillog(6,host.id,host.hostname,env.host,'Needed to prompt for a connection or sudo password')

        if 'Timed out' in str(ret[env.host]):
            return self.faillog(1,host.id,host.hostname,env.host,ret[env.host])
        elif 'No route to host' in str(ret[env.host]):
            return self.faillog(4,host.id,host.hostname,env.host,ret[env.host])
        elif 'Connection refused' in str(ret[env.host]):
            return self.faillog(5,host.id,host.hostname,env.host,ret[env.host])
        elif 'Connection reset by peer' in str(ret[env.host]):
            return self.faillog(7,host.id,host.hostname,env.host,ret[env.host])
        elif 'Underlying exception' not in str(ret[env.host]):
            return ret
        else:
            return self.faillog(2,host.id,host.hostname,env.host,ret[env.host])

    def fabric_hard(self):
        disk_list = []
        disks = run(
        "fdisk -l 2>/dev/null |grep 'Disk /dev'|awk '{split($2,s,\":\"); print substr(s[1], 6), $3, substr($4,1,2);}'").split(
        '\r\n')
        total_size = 0
        for disk in disks:
            disk_info = {}
            d = disk.split()
            disk_info = {d[0]: d[1] + " " + d[2]}
            disk_list.append(disk_info)
            if d[2] == 'MB':
                d[1]=int(round(float(d[1]) / 1000.0))
            elif d[2] == 'GB':
                d[1]=int(round(float(d[1])))
            total_size += d[1]

        cpu_core = int(run("cat /proc/cpuinfo |grep 'processor' |wc -l"))

        mem_size = int(run("free -m |awk '/Mem/ {print $2}'"))
        memory = int(round(mem_size / 1000.0))

        return (cpu_core, memory, total_size)

    def fabric_ifconfig(self):
        return run('/sbin/ifconfig')

    def fabric_ipmitool(self):
        return run('modprobe ipmi_devintf ; modprobe ipmi_si ; /usr/bin/ipmitool lan print')

    def faillog(self,type,hostid,hostname,ip,msg):
        if hostid in self.fail_hostids:
            return False
        msglog = {
            'id':hostid,
            'hostname':hostname,
            'tips':[str(msg)]
        }
        self.fail_hostids.append(hostid)
        self.messages['fail'].append(msglog)
        return False