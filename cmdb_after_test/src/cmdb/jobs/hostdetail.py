# -*- coding: utf-8 -*-
from models.pool import Pool
from models.host import Host
from models.device import Device
from models.user import User
from models.pool_host import PoolHost
from models.host_load_daily import HostLoadDaily
from models.ip_address import IpAddress
from application import db
from sqlalchemy import and_,desc
import csv

class HostDetail:
    def run(self):
        print "===========start==========="
        self.test()
        print "===========end============="


    def test(self):
        pool_info = Pool.query.order_by(desc(Pool.id)).first()
        print "============"
        print pool_info.name
        info = db.session.query(Pool.id,Pool.name,User.cn_name ,Host.hostname,Host.cpu,Host.memory,Host.storage,Device.buy_time,IpAddress.ipv4).filter(and_(PoolHost.pool_id == Pool.id,PoolHost.host_id == Host.id,Host.device_id == Device.id,Pool.team_owner == User.id,Host.deleted == 0,Host.primary_ip_id == IpAddress.id)).all()
        csvfile = open('hostdetail.csv', 'wb')
        spamwriter = csv.writer(csvfile,dialect='excel')
        spamwriter.writerow(["主机名","IP","pool名称","业务负责人","cpu/核","内存/G","硬盘/G","购买时间"])
        data = []
        for item in info:
            host_radio = HostLoadDaily.query.filter(HostLoadDaily.host_id == item.id).order_by(desc(HostLoadDaily.id)).first().ratio
            data.append((item.hostname,item.ipv4,item.name,item.cn_name,str(item.cpu),str(item.memory),str(item.storage),str(item.buy_time),str(host_radio)))
        for a in data:
            spamwriter.writerow(a)

        csvfile.close()



