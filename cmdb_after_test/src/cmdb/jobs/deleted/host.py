# -*- coding: utf-8 -*-
from __future__ import with_statement
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")#加入默认的扫描路径

import json,time
from sqlalchemy import and_
from flask.ext.script import Manager
from fabric.api import *
from application import app, db
from models.host import Host
from models.ip_address import IpAddress
from views.pool import get_ansible_passwd
from views.host import _operation_log
from tasks import host_device_changed


manager = Manager(app)

env.user = 'root'
#env.password = '%s'%get_ansible_passwd().strip()
env.password = 'anjukeansible'
env.key_filename = '/root/.ssh/ansible_rsa'
env.warn_only = True
env.time_out = 3
env.skip_bad_hosts = True
env.abort_on_prompts = True
env.abort_exception = True


@manager.command
def monitor():
    black=[]
    hosts = Host.query.filter(and_(Host.deleted == Host.DELETED_NO,Host.id>0)).order_by(Host.id.desc()).all()
    for host in hosts:
        time.sleep(3)
        if host.id in black:
            continue
        print '------ID:%s,Hostname:%s--------'%(host.id,host.hostname)
        host_ip = IpAddress.query.filter(IpAddress.id == host.primary_ip_id).first()
        if host_ip:
            env.host = '%s'%host_ip.ipv4
            try:
                host_info = execute(fabric_host, host=env.host)
            except:
                faillog(6,host.id,host.hostname,env.host,'Needed to prompt for a connection or sudo password')
                continue
            if 'Timed out' in str(host_info[env.host]):
                faillog(1,host.id,host.hostname,env.host,host_info[env.host])
            elif 'No route to host' in str(host_info[env.host]):
                faillog(4,host.id,host.hostname,env.host,host_info[env.host])
            elif 'Connection refused' in str(host_info[env.host]):
                 faillog(5,host.id,host.hostname,env.host,host_info[env.host])
            elif 'Underlying exception' not in str(host_info[env.host]):
                cpu=host_info[env.host][0]
                memory=host_info[env.host][1]
                storage=host_info[env.host][2]
                log_data={}
                if host.cpu != cpu:
                     log_data['cpu']="cpu从 %s 更改为 %s"%(host.cpu,cpu)
                     host.cpu = cpu
                if host.memory != memory:
                     log_data['memory']="memory %s 更改为 %s"%(host.memory,memory)
                     host.memory = memory
                if host.storage != storage:
                     log_data['storage']="storage %s 更改为 %s"%(host.storage,storage)
                     host.storage = storage
                if log_data:
                    log = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
                    _operation_log(host.id, 0, log)
                host_device_changed.delay(host.id, 1, 1)
                db.session.add(host)
                db.session.commit()
            else:
                faillog(2,host.id,host.hostname,env.host,host_info[env.host])
        else:
            faillog(3,host.id,host.hostname,env.host,'No ip')


def fabric_host():
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

def abort(msg):
    print "================"
    print msg

def faillog(type,hostid,hostname,ip,msg):
    output = open('/tmp/cmdb_fail.txt', 'a')
    try:
        output.write('fail[type:%s]:ID:%s,HOSTNAME:%s,IP:%s,MSG:%s\r\n'%(type,hostid,hostname,ip,msg))
    finally:
        output.close()

if __name__ == "__main__":
    manager.run()




