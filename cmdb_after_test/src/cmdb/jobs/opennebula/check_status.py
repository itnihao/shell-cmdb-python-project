#-*- coding: UTF-8 -*-
from application import db,app
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../../")
from sqlalchemy import and_
from models.apply_host import Apply_host
from models.apply import Apply
from models.user import User
from models.host import Host
from models.host_ip import  HostIp
from config import MAIL_TO,DOMAIN,CREDENTIALS,ENDPOINT
from models import IpAddress
from models.apply_host_tasks import ApplyHostTasks
from models.log import Log
from models.host_bastion_apply import HostBastionApply
from models.dns.dns_apply import DnsApply
from models.dns.dns_tasks import DnsTasks
from models.dns.dns_zone import DnsZone
from models.host_bastion_tasks import HostBastionTasks
from models.pool import Pool
from models.pool_host import PoolHost
from views.oca import Client
from views.host import _operation_log
from views.functions import _set_used_ip
from views.functions import  addmail
from views.bastion import add_authority
from main import CMDB_VM
from signal import signal, SIGTERM
import datetime,json
import os,sys,atexit

PID_FILE = '/var/run/cmdb_host_check.pid'

def atexit_removepid(pid_file):
    try:
        os.remove(pid_file)
    except:
        pass
    print '---------end--------------'

class check_status:
    def run(self):
        print '---------start--------------'
        client = Client(CREDENTIALS, ENDPOINT)
        if self.is_runing():
            sys.exit(1)
        self.check(client)
        self.update_apply_status()

    def is_runing(self):
        pid_file = PID_FILE
        if os.path.isfile(pid_file):
            print("The program is running")
            return 1
        else:
          try:
            signal(SIGTERM, lambda signum, stack_frame: exit(1))
            atexit.register(lambda:atexit_removepid(pid_file))
            fd=os.open(pid_file,os.O_CREAT|os.O_EXCL|os.O_RDWR)
            os.write(fd,"%s\n" % os.getpid())
            os.close(fd)
            return 0
          except:
            print("Cann't get a lock file")
            return 1

    def check(self,client):
        task = Apply_host.query.filter(Apply_host.status == 1).all()
        for item in task:
            vm = CMDB_VM(client)
            apply_info = Apply.query.filter(Apply.id == item.apply_id).first()
            vm_info = vm.get_vm_info(item.vm_id)
            not_check_status = [-2,-1,0,1,2,4,5,6]
            if vm_info['state'] in not_check_status:
                continue
            if vm_info['state'] == '3':
                item.status = 3
                db.session.commit()
                hostname = self.get_hostname(item.host_id)
                config_info = eval(apply_info.template)
                host_info = Host.query.filter(Host.id == item.host_id).first()
                ipinfo = IpAddress.query.filter(IpAddress.ipv4 == vm_info['IP']).first()
                host_info.deleted = 0
                host_info.note = apply_info.content
                host_info.cpu = config_info['cpu']
                host_info.memory = config_info['mem']
                host_info.storage = config_info['disk']
                host_type = host_info.type_descri
                apc_ip = self.get_host_ip(item.apc_id)
                host_info.search = "%s#@#%s#@#%s#@#%s#@#%sCore#@#%sG#@#%sG#@#%s"%(hostname, host_type, apc_ip,  vm_info['IP'],
                                                    config_info['cpu'], config_info['mem'], config_info['disk'], apply_info.content)
                db.session.commit()
                pool_host_info = PoolHost(apply_info.pool_id,item.host_id)
                db.session.add(pool_host_info)
                db.session.commit()

                if ipinfo:
                    _set_used_ip(ipinfo.id, IpAddress.FLAG_USED, IpAddress.TYPE_HOST, item.host_id)
                    host_info.primary_ip_id = ipinfo.id
                    db.session.commit()
                    target = HostIp(item.host_id,0,ipinfo.id)
                    db.session.add(target)
                    db.session.commit()
                    dns_zone_info = DnsZone.query.filter(DnsZone.zone == "i.ajkdns.com").first()
                    zone_id = dns_zone_info.id
                    dns_apply_info = DnsApply.query.filter(and_(DnsApply.prefix == "update",DnsApply.zone_id==zone_id)).first()
                    dns_apply_id = dns_apply_info.id
                    dns_task_target = DnsTasks(dns_apply_id=dns_apply_id, type=1, status=0)
                    db.session.add(dns_task_target)
                    db.session.commit()
                else:
                    subject = "开通主机%s成功,更新host表失败"%(hostname)
                    content = "主机:%s<br>IP:%s<br>更新apply_host表失败,原因是在ipaddress表里面找不到%s.请手动更新并在" \
                              "ipaddress,hostip表里面标明占用信息"\
                              %(hostname,vm_info['ip'],vm_info['ip'])
                    addmail(MAIL_TO['mail_receiver'],subject,content)
                    time = self.now_time()
                    print time,content
                type = HostBastionApply.TYPE_HOST
                add_authority(apply_info.uid,type,host_info.id,HostBastionApply.ROLE_ROOT,apply_info.approver_uid,HostBastionApply.STATUS_RUNNING,30,"申请主机开通权限")
            elif vm_info['state'] == '7':
                self.del_host(item.host_id)
                item.status = 7
                db.session.commit()

    def update_apply_status(self):
        apply_info = Apply.query.filter(Apply.status == 3).all()
        for item in apply_info:
            apply_host_pendding = Apply_host.query.filter(and_(Apply_host.apply_id == item.id,Apply_host.status == 1)).all()
            apply_task =  ApplyHostTasks.query.filter(ApplyHostTasks.apply_id == item.id).first()
            if apply_task.status == 0:
                continue
            if apply_host_pendding:
                continue
            apply_host_info = Apply_host.query.filter(and_(Apply_host.apply_id == item.id,Apply_host.status == 3)).all()
            apply_task_info = ApplyHostTasks.query.filter(ApplyHostTasks.apply_id == item.id).first()
            host_infos = []
            hostnames = []
            if apply_host_info:
                for apply_host in apply_host_info:
                    hostname  = self.get_hostname(apply_host.host_id)
                    host_ip = self.get_host_ip(apply_host.host_id)
                    tmp = {'id':apply_host.host_id,'name':hostname,'ip':host_ip}
                    host_infos.append(tmp)
                    hostnames.append(hostname)
            success_num = len(apply_host_info)
            config = eval(item.template)
            config_info = "%s核/%sG/%sG/%s"%(config['cpu'],config['mem'],config['disk'],config['os'])
            if item.num == success_num:
                reciver =  User.query.filter(User.id == item.uid).first().email
                subject = "[主机申请]您申请的%s台主机开通成功" %item.num
                content = ""
                for host_info in host_infos:
                    content += " 主机:<a href='" + str(DOMAIN) + "/cmdb/host/%s"%(host_info['id']) +"'>" + host_info['name'] +"</a>" + \
                               "  IP:<a href='"+ str(DOMAIN) + "/cmdb/host/%s"%(host_info['id']) +"'>" +host_info['ip']+\
                               "</a>  配置:%s <br>" %(config_info)
                addmail(reciver,subject,content)
                item.status = 4
                db.session.commit()
                time = self.now_time()
                print time,content
                uid = item.uid
                log = "申请了%s台主机,主机名：%s" %(item.num,','.join(hostnames))
                self.addlog(uid,log)
            else:
                item.status = 5
                db.session.commit()
                apply_task_info.status == 2
                username =  User.query.filter(User.id == item.uid).first().cn_name
                subject = "[主机申请]%s申请的主机开通状态" %(username)
                if success_num:
                    content = "申请了%s台主机,开通了%s台</br>"%(item.num,success_num)
                    for host_info in host_infos:
                        content += " 主机:<a href='" + str(DOMAIN) + "/cmdb/host/%s"%(host_info['id']) +"'>" + host_info['name'] +"</a>" + \
                                " IP:<a href='"+ str(DOMAIN) + "/cmdb/host/%s"%(host_info['id']) +"'>" +host_info['ip']+\
                               "</a> 配置:%s <br>" %(config_info)
                    fail_num = item.num - success_num
                    content += "<br>失败了%s台"%(fail_num)
                    content += "<br>申请id:%s" %(item.id)
                else:
                      content = "%s申请了%s台主机，全部开通失败 申请id:%s  配置:%s</br>"%(username,item.num,item.id,config_info)
                addmail(MAIL_TO['mail_receiver'],subject,content)
                time = self.now_time()
                print time,content
            self.add_host_log(host_infos,config,item.id,item.pool_id,item.uid)

    def get_hostname(self,hostid):
        host_info = Host.query.filter(Host.id == hostid).first()
        return host_info.hostname

    def get_host_ip(self,host_id):
        ip_id = Host.query.filter(Host.id == host_id).first().primary_ip_id
        ipv4 = ""
        ip_info = IpAddress.query.filter(IpAddress.id == ip_id).first()
        if ip_info:
            ipv4 = ip_info.ipv4
        return ipv4

    def add_host_log(self,hostinfos,config,applyid,poolid,uid):
        username = User.query.filter(User.id == uid).first().cn_name
        approver_uid = app.config.get("APPROVER")['host']
        pool_name = Pool.query.filter(Pool.id == poolid).first().name
        for host_info in hostinfos:
            log_data = {}
            log_data['status']  = '状态 从 可使用 更改为 已分配(申请人: %s 申请id:%s  pool: %s 配置: %s核/%sG/%sG 操作系统:%s)'%(username,
                                            applyid,pool_name,config['cpu'],config['mem'],config['disk'],config['os'])
            content = json.dumps(log_data, ensure_ascii=False, separators=(',', ':')).encode('utf8')
            _operation_log(host_info['id'],approver_uid,content)

    #根据hostid删除主机
    def del_host(self,hostid):
        host_info = Host.query.filter(Host.id == hostid).first()
        #db.session.delete(host_info)
        host_info.deleted = Host.DELETED_YES
        db.session.commit()
        apply_host_info = Apply_host.query.filter(Apply_host.host_id == hostid).first()
        db.session.delete(apply_host_info)
        db.session.commit()

    def now_time(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time

    def addlog(self,uid,content,flag=1):
        username = User.query.filter(User.id == uid).first()
        content="用户:%s%s" %(username.cn_name,content)
        logtarget=Log(uid,flag,content)
        db.session.add(logtarget)
        db.session.commit()