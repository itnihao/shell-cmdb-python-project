# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../../")
from views.oca import Client
from views.oca.host import Host, HostPool
from views.oca.vm import VirtualMachine, VirtualMachinePool
from views.oca.cluster import Cluster, ClusterPool
from views.oca.user import User, UserPool
from views.oca.image import Image, ImagePool
from views.oca.vn import VirtualNetwork, VirtualNetworkPool
from views.oca.exceptions import OpenNebulaException
from xml.etree.ElementTree import Element as EL
from application import app

def format_host(host):
    import math
    standard_unit =1024
    id = host.id
    name = host.name
    tp = host.host_share
    cpu_usage =tp.cpu_usage
    real_cpu_usage = tp.used_cpu
    free_cpu = tp.free_cpu
    total_cpu = tp.max_cpu

    mem_usage = math.ceil( int(tp.mem_usage) / standard_unit )
    real_mem_usage = math.ceil( int(tp.used_mem) / standard_unit )
    free_mem = math.ceil( int(tp.free_mem )/ standard_unit )
    total_mem =  math.ceil( int(tp.max_mem) / standard_unit )

    disk_usage = math.ceil( int(tp.disk_usage) / standard_unit )
    real_disk_usage = math.ceil( int(tp.used_disk) / standard_unit )
    free_disk = math.ceil( int(tp.free_disk) / standard_unit )
    total_disk = math.ceil( int(tp.max_disk) / standard_unit )

    return {
        'id':id,
        'name':name,
        'cpu':{
            'usage':cpu_usage,
            'real_usage':real_cpu_usage,
            'free':free_cpu,
            'total':total_cpu
        },
        'mem':{
            'usage':mem_usage,
            'real_usage':real_mem_usage,
            'free':free_mem,
            'total':total_mem
        },
        'disk':{
            'usage':disk_usage,
            'real_usage':real_disk_usage,
            'free':free_disk,
            'total':total_disk
        }
    }



class CMDB_VM():
    def __init__(self,client):
        self.client = client

    def create_vm(self,**kwargs):
        fp = open("template")
        template = fp.read()
        for change_name,val in kwargs.items():
            change_name = "#%s#"%change_name.upper()
            template = template.replace(change_name,'%s'%val)
        vm_id = VirtualMachine.allocate(self.client,template)
        return vm_id

    def info(self,filter=-3, range_start=-1, range_end=-1, vm_state=-1):
        vp = VirtualMachinePool(self.client)
        vp.info(filter, range_start, range_end, vm_state)


    def get_vm_info(self,vm_id):
        xml = '''<?xml   version="1.0"   encoding="utf-8"?>
<TEMPLATE>
<ID>%d</ID>
</TEMPLATE>
    '''%vm_id
        vm = VirtualMachine(xml,self.client)
        vm.info(vm_id)
        net = vm.xml.find('TEMPLATE') .find('NIC')
        ip = net.findtext('IP')
        state = vm.xml.findtext('STATE')
        data = {'IP':ip,'state':state,'vm_id':vm_id}
        return data


    def deploy(self,vm_id,host_id):
        xml = '''<?xml   version="1.0"   encoding="utf-8"?>
<TEMPLATE>
<ID>%d</ID>
</TEMPLATE>
    '''%vm_id
        vp = VirtualMachine(xml,self.client)
        vp.deploy(host_id)


class CMDB_HOST():
    def __init__(self,client):
        self.client = client

    @staticmethod
    def hostpool(client):
        hp = HostPool(client)
        hp.info()
        data = []
        for item in hp.xml:
            ht = hp.factory(item)
            item_data = format_host(ht)
            #tp = ht.host_share
            # print ht.name,tp.mem_usage
            info = {'node':item_data['name'],'node_mem_used':item_data['mem']['usage'],'node_info':item_data}
            data.append(info)
        return  data

    def hostinfo(self):
        xml = '''<?xml   version="1.0"   encoding="utf-8"?>
<TEMPLATE>
<ID>6</ID>
</TEMPLATE>'''
        h =  Host(xml,self.client)
        h.info()
        print h.id
        tp = h.__getattr__("TEMPLATE")
        for item in tp:
            print item.tag,item.text


class CMDB_VN():
    def __init__(self,client,idc):
        self.client = client
        self.idc = idc

    def available_vn(self,client,idc,filter=-3, range_start=-1, range_end=-1):
        clusters = app.config.get('CLUSTER_NAME')
        cluster = clusters[str(idc)]
        vnp = VirtualNetworkPool(client)
        vnp.info(filter, range_start, range_end)
        data = []
        for item in vnp.xml:
            vn = vnp.factory(item)
            vm_id = vn.id
            if vn.cluster == cluster:
                total = self.vninfo(client,vm_id)
                if int(total) > int(vn.TOTAL_LEASES):
                    data = {'vnid':vm_id,'vnname':vn.name}
                    break
        return data


    def vninfo(self,client,vm_id):
        xml = '''<?xml   version="1.0"   encoding="utf-8"?>
<TEMPLATE>
<ID>%s</ID>
</TEMPLATE>'''%vm_id
        vn_info =  VirtualNetwork(xml,client)
        vn_info.XML_TYPES= {
            'id'       : int,
            'uid'      : int,
            'name'     : str,
            'leases'  : EL
         }
        vn_info.info()
        h = vn_info.__getattr__('LEASES')
        return len(h)

    # @staticmethod
    # def available_vn(client,filter=-3, range_start=-1, range_end=-1):
    #     vnp = VirtualNetworkPool(client)
    #     vnp.info(filter, range_start, range_end)
    #     for item in vnp.xml:
    #         vn = vnp.factory(item)
    #         ar = item.ar_pool
    #          print item.find('VNET')
    #         name = vn.name
    #         total_ips = len(ar.tag.findall("AR"))
    #         used_ips = vn.used_leases
    #         if total_ips > used_ips:
    #             return name
    #             break
