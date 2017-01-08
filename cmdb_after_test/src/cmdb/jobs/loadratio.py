# -*- coding: utf-8 -*-
from application import app,db
from sqlalchemy import and_
from models.host import Host
from models.host_load_ratio import HostLoadRatio
from models.pool_load_ratio import PoolLoadRatio
from models.pool_host import PoolHost
from models.ip_address import IpAddress
from models.pool import Pool
from models.host_ip import HostIp
import urllib,json, datetime,time



class LoadRatio:
    def run(self):
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.hosts_load = {}
        self.host_load()
        self.pool_load()
        #self.test_pool_load()

    def host_load(self):
        import socket
        socket.setdefaulttimeout(2)
        hosts_load = {}
        host_info = Host.query.filter(Host.deleted == 0).all()
        for host_item in host_info:
            high_ratio = 0
            high_key = ''
            load_dict = {
                'cpu_1': 0,
                'iowait': 0,
                'disk_used': 0,
                'mem_used': 0,
                'net': 0,
            }
            item_ratio = {
                'cpu_1': 0.05,
                'iowait': 0.05,
                'disk_used': 0.05,
                'mem_used': 0.05,
                'net': 0.05
            }
            hostname = host_item.hostname
            host_info = Host.query.filter(Host.hostname == hostname).first()
            if host_info:
                host_id = host_info.id
            info = db.session.query(Host.id,IpAddress.ipv4).filter(and_(HostIp.host_id == Host.id),(HostIp.ip_address_id==IpAddress.id),(Host.id == host_id)).first()
            if info:
                ipv4 = info.ipv4
                try:
                    if ipv4.split('.')[1] == '10':
                        data = {'hostname':hostname}
                        f = urllib.urlopen(url=app.config.get('ZABBIX_API_URL_10'),data = urllib.urlencode(data))
                    elif ipv4.split('.')[1] == '20':
                        data = {'hostname':hostname}
                        f = urllib.urlopen(url=app.config.get('ZABBIX_API_URL_20'),data = urllib.urlencode(data))
                    else:
                        data = {'hostname':hostname}
                        f = urllib.urlopen(url=app.config.get('ZABBIX_API_URL'),data = urllib.urlencode(data))
                except Exception:
                    continue
                try:
                    monitor_info = json.loads(f.read())
                except (TypeError, ValueError) as err:
                    monitor_info = {'code':1}
                    print 'ERROR(%s):%s'%(err,hostname)
                if monitor_info['code'] == 0:
                    monitor_data = monitor_info['data']
                    if monitor_data.has_key('cpu_1'):
                        load_dict['cpu_1'] = float(monitor_data['cpu_1']['value'])
                        if load_dict['cpu_1'] >= high_ratio:
                            high_ratio = load_dict['cpu_1']
                            high_key = 'cpu_1'
                    if monitor_data.has_key('iowait'):
                        tmp_iowait = float(monitor_data['iowait']['value'])
                        load_dict['iowait'] = float('%.2f'%(tmp_iowait/100.0))
                        if load_dict['iowait'] >= high_ratio:
                            high_ratio = load_dict['iowait']
                            high_key  = 'iowait'
                    if monitor_data.has_key('net_in') and monitor_data.has_key('net_out'):
                        net_in = float(monitor_data['net_in']['value'])
                        net_out = float(monitor_data['net_out']['value'])
                        tmp_net_high = net_in
                        if net_out > net_in:
                            tmp_net_high = net_out
                        load_dict['net'] = float('%.2f'%(tmp_net_high/1000))
                        if load_dict['net'] >= high_ratio:
                            high_ratio = load_dict['net']
                            high_key = 'net'

                    if monitor_data.has_key('total_disk_used') and type(monitor_data['total_disk_used'])==dict:
                        tmp_total_disk_used = float(monitor_data['total_disk_used']['value'])
                        load_dict['disk_used'] = float('%.2f'%(tmp_total_disk_used/100.0))
                        if load_dict['disk_used'] >= high_ratio:
                            high_ratio = load_dict['disk_used']
                            high_key  = 'disk_used'

                    if monitor_data.has_key('available_mem_rate'):
                        load_dict['mem_used'] = float((100-monitor_data['available_mem_rate']['value'])/100.0)
                        if load_dict['mem_used'] >= high_ratio:
                            high_key  = 'mem_used'


            item_ratio[high_key] = 0.8
            host_ratio = 0
            for key,value in load_dict.items():
                host_ratio = float(host_ratio) + float(value) * float(item_ratio[key])

            host_ratio = '%.2f'%host_ratio

            hosts_load['host_%s'%host_id] = host_ratio

            content = json.dumps(load_dict)
            target = HostLoadRatio(host_id,host_ratio,content,self.created)
            db.session.add(target)
            db.session.commit()

        self.hosts_load = hosts_load



    def pool_load(self):
        hosts_load =self.hosts_load
        pool_list = Pool.query.all()
        if pool_list:
            for item in pool_list:
                tmp_pool_load = 0.0
                tmp_pool_id = item.id
                hosts = PoolHost.query.filter(PoolHost.pool_id == tmp_pool_id).all()
                if hosts:
                    tmp_ratio = 0.0
                    for item_host in hosts:
                        if hosts_load.has_key('host_%s'%item_host.host_id):
                            tmp_ratio += float(hosts_load['host_%s'%item_host.host_id])
                    tmp_pool_load = tmp_ratio/len(hosts)
                    tmp_pool_load = float('%.2f'%tmp_pool_load)

                target = PoolLoadRatio(tmp_pool_id,tmp_pool_load,self.created)
                db.session.add(target)
                db.session.commit()
                print 'Pool:%s,Ratio:%s'%(tmp_pool_id,tmp_pool_load)


    def test_pool_load(self):
        hosts_load = {}
        hosts_load_list = HostLoadRatio.query.all()

        for item in hosts_load_list:
            hosts_load['host_%s'%item.host_id] = item.ratio

        pool_list = Pool.query.all()
        if pool_list:
            for item in pool_list:
                tmp_pool_load = 0.0
                tmp_pool_id = item.id
                hosts = PoolHost.query.filter(PoolHost.pool_id == tmp_pool_id).all()
                if hosts:
                    tmp_ratio = 0.0
                    for item_host in hosts:
                        if hosts_load.has_key('host_%s'%item_host.host_id):
                            tmp_ratio += float(hosts_load['host_%s'%item_host.host_id])
                    tmp_pool_load = tmp_ratio/len(hosts)
                    tmp_pool_load = float('%.2f'%tmp_pool_load)

                target = PoolLoadRatio(tmp_pool_id,tmp_pool_load,self.created)
                db.session.add(target)
                db.session.commit()

                print 'Pool:%s,Ratio:%s'%(tmp_pool_id,tmp_pool_load)



