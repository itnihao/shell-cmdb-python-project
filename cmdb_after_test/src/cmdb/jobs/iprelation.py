# -*- coding: utf-8 -*-

from application import db
from models.host_ip import HostIp
from models.device_ip import DeviceIp
from models.ip_address import IpAddress


class IpRelation:
    def run(self):
        ip = IpAddress.query.filter(IpAddress.flag == 1).order_by(IpAddress.id).all()
        for item in ip:
            device = DeviceIp.query.filter(DeviceIp.ip_address_id == item.id).first()
            if device:
                item.type = 2
                item.target_id = device.device_id
                db.session.commit()
            else:
                host = HostIp.query.filter(HostIp.ip_address_id == item.id).first()
                if host:
                    item.type = 1
                    item.target_id = host.host_id
                    db.session.commit()
                else:
                    print("=====")
                    print(item.ipv4)
                    print("已占用，未关联")
                    item.flag = 0
                    db.session.commit()
        return
