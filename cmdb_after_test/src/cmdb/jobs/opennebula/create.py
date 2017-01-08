#-*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../../")
from models.apply import Apply
from models.host import Host
from models.pool_host import PoolHost
from models.apply_host import Apply_host
from models.device import Device
from models.apply_host_tasks import ApplyHostTasks
from models.rack import Rack
from models.user import User
from main import CMDB_VM
from main import CMDB_HOST
from main import CMDB_VN
from views.functions import  addmail
from config import MAIL_TO,CREDENTIALS,ENDPOINT
from application import db,app
from sqlalchemy import and_
from views.host import get_host_name
import datetime
from views.oca import Client
from signal import signal, SIGTERM
import os,sys,atexit

PID_FILE = '/var/run/cmdb_host_create.pid'

def atexit_removepid(pid_file):
    try:
        os.remove(pid_file)
    except:
        pass
    print '---------end--------------'

class create:
    def run(self):
        print '---------start--------------'
        client = Client(CREDENTIALS, ENDPOINT)
        sys.exit(self.start(client))

# status = 3 资源不足
    def start(self,client):
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
          except:
            print("Cann't get a lock file")
            return 1
        task = self.__unruninfo(client)
        for item in task:
            for i in range(item.num):
                except_apc_id = self._get_pool_apcid(item.pool_id)
                apc_info = self.__get_idc_hosts(client,item.idc,except_apc_id)
                if apc_info:
                    resoure = self.__choose_best_hostid(apc_info,item.template)
                    if resoure['apc_id'] == 0:
                        data = self.__all_apc_info(client,item,i)
                        if data['code'] == 0:
                            break
                        else:
                            resoure = data['resoure']
                else:
                    data = self.__all_apc_info(client,item,i)
                    if data['code'] == 0:
                        break
                    else:
                        resoure = data['resoure']
                self.__create_vm(client,resoure['hostid'],resoure['apc_id'],item.template,item.idc,item)

    def __all_apc_info(self,client,item,i):
        config = eval(item.template)
        config_info = "%s核/%sG/%sG/%s"%(config['cpu'],config['mem'],config['disk'],config['os'])
        apc_info = self.__get_idc_hosts(client,item.idc)
        resoure = self.__choose_best_hostid(apc_info,item.template)
        data = {'code':1,'resoure':resoure}
        if resoure['apc_id'] == 0:
            apply_info = Apply.query.filter(Apply.id == item.apply_id).first()
            username = User.query.filter(User.id == apply_info.uid).first()
            reciver = MAIL_TO['mail_receiver']
            subject = "宿主机资源不足,虚拟机开通失败"
            content = "%s 申请的%s台机器"%(username.cn_name,item.num)
            if i > 0:
                content += "%s台有资源"%(i)
            else:
                fail_num = item.num - i
                content += "%s台没有资源"%(fail_num)
            content += " 申请id:%s" %(item.apply_id)
            content += " 配置:%s"%config_info
            time = self.now_time()
            print time,content
            addmail(reciver,subject,content)
            item.status = 3
            db.session.commit()
            apply_info.staus = 5
            db.session.commit()
            data['code'] = 0
        return data

    def __unruninfo(self,client):
        info = ApplyHostTasks.query.filter(ApplyHostTasks.status == 0).all()
        return info

# 在特定宿主机上面开通虚拟机
    def __create_vm(self,client,hostid,apcid,template,idc,task):
        task.status = 1
        vm_create = CMDB_VM(client)
        host_name = self.__get_host_name(idc,apcid)
        host_id = self.__get_hostid(host_name)
        vn_info = self.__get_available_vn(client,idc)
        if vn_info:
            print vn_info
            vn_name = vn_info['vnname']
            needs = eval(template)
            if idc == 1:
                idc_name = "idc10"
            else:
                idc_name = "idc20"
            image_name = idc_name + '-' +  needs['os'] + '.qcow2'
            vm_id = vm_create.create_vm(NAME = host_name, CPU = needs['cpu'], VCPU = needs['cpu'], MEMORY = needs['mem'] * 1024,
                                        DISK=needs['disk'] * 1024,NETWORK=vn_name,IMAGE_NAME=image_name)
            if vm_id:
                vm_create.deploy(vm_id,hostid)
                target = Apply_host(apply_id=task.apply_id, vm_id=vm_id,apc_id=apcid, host_id=host_id)
                db.session.add(target)
                db.session.commit()
            else:
                self.__del_host(host_name)
                reciver = MAIL_TO['mail_receiver']
                subject = "[主机申请]虚拟机开通失败,api没有返回vm_id"
                content = "开通%s失败，原因是api没有返回vm_id！<br>" %(host_name)
                content += "<br>申请id:%s" %(task.apply_id)
                time = self.now_time()
                print time,content
                addmail(reciver,subject,content)
        else:
            self.__del_host(host_name)
            reciver = MAIL_TO['mail_receiver']
            subject = "[主机申请]虚拟机开通失败,没有可用的网络资源"
            content = "开通%s失败，原因是idc%d0没有可用的网络资源！<br>" %(host_name,idc)
            content += "<br>申请id:%s" %(task.apply_id)
            time = self.now_time()
            print time,content
            addmail(reciver,subject,content)

#根据主机名删除主机
    def __del_host(self,host_name):
        host_info = Host.query.filter(Host.hostname == host_name).first()
        #db.session.delete(host_info)
        host_info.deleted = Host.DELETED_YES
        db.session.commit()
        apply_host_info = Apply_host.query.filter(Apply_host.host_id == host_info.id).first()
        db.session.delete(apply_host_info)
        db.session.commit()



#返回hostid
    def __get_hostid(self,host_name):
        host_info = Host.query.filter(Host.hostname == host_name).first()
        return host_info.id

#获取开通虚拟机的名字
    def __get_host_name(self,idc,apcid):
        if idc == 1:
            q = 'xapp10'
        if idc == 3:
            q = 'xapp20'
        ret = False
        ret = get_host_name(q)
        if ret:
            ret = ret[0][1]
            target = Host(hostname=ret, primary_ip_id=0, type=1, is_virtual=1, parent_id=apcid, device_id=0, status=3, cpu=0, memory=0, storage=0, note="",deleted=1)
            db.session.add(target)
            db.session.commit()
        return ret

#获取一个可用的network
    def __get_available_vn(self,client,idc):
        vn = CMDB_VN(client,idc)
        vn_info = vn.available_vn(client,idc)
        return vn_info

#除去特定宿主机的opennebula资源
    def __get_idc_hosts(self,client,idc,except_apc_id=[]):
        data = []
        host_pool = CMDB_HOST(client)
        info  =  host_pool.hostpool(client)
        for item in info:
            host_name = item['node']
            if except_apc_id:
                host_info = Host.query.filter(and_(Host.hostname == host_name,Host.deleted == 0,~Host.id.in_(except_apc_id))).first()
            else:
                host_info = Host.query.filter(and_(Host.hostname == host_name,Host.deleted == 0)).first()
            if  host_info:
                device_info = Device.query.filter(Device.id == host_info.device_id).first()
                rack_info = Rack.query.filter(Rack.id == device_info.rack_id).first()
                if rack_info.datacenter_id == idc:
                    info = {'node':host_name,'node_mem_used':item['node_mem_used'],'node_info':item['node_info'],'cmdb_host_id':host_info.id}
                    data.append(info)
        return  data

#获取pool下面虚拟机的宿主机id
    def _get_pool_apcid(self,pool_id):
        apc_id = []
        pool_host_info = PoolHost.query.filter(PoolHost.pool_id == pool_id).all()
        for item in pool_host_info:
            host_info = Host.query.filter(Host.id == item.host_id).first()
            if host_info.is_virtual == 1:
                apc_id.append(host_info.parent_id)
        return apc_id

#默认按内存资源优先
    def __choose_best_hostid(self,data,template):
        needs = eval(template)
        hostid = 0
        apcid = 0
        tmp_data = {'apc_id':apcid,'hostid':hostid,'mem':0}
        for item in data:
            free_mem = int(item['node_info']['mem']['total']) -  int(item['node_info']['mem']['usage'])
         #   free_cpu = int(item['node_info']['cpu']['total']) -  int(item['node_info']['cpu']['usage'])
            if free_mem >= (int(needs['mem']) * 1024) and free_mem > tmp_data['mem']:
                tmp_data = {'hostid':item['node_info']['id'],'apc_id':item['cmdb_host_id'],'mem':free_mem}
        return tmp_data

    def now_time(self):
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time
