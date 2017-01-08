# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import DDNS_MIGRATE_DATABASE_URI
from config import DNSAPPLY_MIGRATE_DATABASE_URI
from models.dns.dns_apply import DnsApply
from models.dns.dns_zone import DnsZone
from models.user import User
from views.user import get_user_id
from application import app, db

class DnsZoneMigrate:
    def run(self):
        db.engine.execute("truncate table dns_zone")
        engine = create_engine(DNSAPPLY_MIGRATE_DATABASE_URI, encoding='utf-8',echo=True)
        connection = engine.connect()
        self.zone_migrate(connection)
        connection.close()

    def zone_migrate(self,connection):
        zone_list = [
                ['d.corp.anjuke.com','OFFICE',1],
                ['a.ajkdns.com','IDC内部',1],
                ['anjuke.com','IDC外部',1],
                ['r.ajkdns.com','IDC外部',0],
                ['anjuke.test','OFFICE',1],
                ['corp.anjuke.com','IDC外部',1],
                ['dev.aifang.com','OFFICE',1],
                ['dev.aifcdn.com','OFFICE',0],
                ['dev.anjuke.com','OFFICE',1],
                ['dev.anjukestatic.com','OFFICE',0],
                ['dev.haozu.com','OFFICE',1],
                ['dev.jinpu.com','OFFICE',1],
                ['dev.xinfang.anjuke.com','OFFICE',0],
                ['fang.anjuke.com','IDC外部',1],
                ['fang.anjuke.test','OFFICE',0],
                ['haozu.com','IDC外部',1],
                ['i.ajkdns.com','IDC外部',0],
                ['jinpu.com','IDC外部',1],
                ['qa.anjuke.com','OFFICE',1],
                ['sp.dev.anjuke.com','OFFICE',0],
                ['xzl.dev.anjuke.com','OFFICE',0],
                ['zu.dev.anjuke.com','OFFICE',0],
                ['dev.ajkcdn.com','OFFICE',0],
                ['dev.sp.anjuke.com','OFFICE',0],
                ['dev.xzl.anjuke.com','OFFICE',0],
                ['dev.zu.anjuke.com','OFFICE',0],
                ['fang.dev.anjuke.com','OFFICE',0]
        ]
        for zone_item in zone_list:
            tmp_zone = zone_item[0]
            tmp_type = 0
            if zone_item[1] == "IDC外部":
                tmp_type = 1
            elif zone_item[1] == "IDC内部":
                tmp_type = 2
            zone_target = DnsZone(uid=502,zone=tmp_zone,type=tmp_type,display=zone_item[2],content="")
            db.session.add(zone_target)
            db.session.commit()



