# -*- coding: utf-8 -*-

from application import db
from models.host import Host
from models.pool import Pool
from models.pool_host import PoolHost
from models.host_ip import HostIp
from sqlalchemy import and_

class ChangeHostStatus:
    def run(self):
        host_ids = []
        hostname = {}
        cnt = 0
        host_info = Host.query.filter(Host.deleted == 0).all()
        for item in host_info:
            host_ids.append(item.id)
            hostname[item.id] = item.hostname
        poolhost_info = db.session.query(PoolHost).filter(PoolHost.host_id.in_(host_ids)).outerjoin(Pool,and_(Pool.source == 3,PoolHost.pool_id == Pool.id)).all()
        print(poolhost_info)
        for item in poolhost_info:
            print(item.host_id)
            print(hostname[item.host_id])
            cnt += 1
        print(cnt)




