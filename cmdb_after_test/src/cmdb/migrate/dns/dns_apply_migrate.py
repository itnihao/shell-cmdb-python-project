# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import DDNS_MIGRATE_DATABASE_URI
from config import DNSAPPLY_MIGRATE_DATABASE_URI
from models.dns.dns_apply import DnsApply
from models.dns.dns_zone import DnsZone
from models.user import User
from sqlalchemy import or_,and_,desc
from views.user import get_user_id
from application import app, db
import re

class DnsApplyMigrate:
    def run(self):
        self.ignore = [
            '*.cms/10.20.6.100/anjuke.test',
            'cms/10.20.6.100/anjuke.test',
            'home/192.168.1.100/dev.anjuke.com',
            '*.kfs/192.168.1.166/dev.anjuke.com',
            'kfs/192.168.1.166/dev.anjuke.com',
            'mobile/192.168.196.218/dev.anjuke.com',
            'broker/192.168.191.45/qa.anjuke.com',
            'amtp/114.80.230.232/anjuke.com',
            'myapi/10.10.6.7/anjuke.com',
            'push/180.153.87.56/anjuke.com',
            'apihome/10.10.6.115/corp.anjuke.com',
            'dba/192.168.1.100/corp.anjuke.com',
            'metrics/192.168.1.95/corp.anjuke.com',
            'sapply/10.10.3.56/corp.anjuke.com',
            'sshkey/192.168.1.100/corp.anjuke.com',
            'drone/192.168.1.24/corp.anjuke.com',
            'dwms/192.168.1.95/corp.anjuke.com',
            'hue/192.168.1.100/corp.anjuke.com',
            'imax/10.20.3.83/corp.anjuke.com',
            'login-pd/10.10.3.235/corp.anjuke.com',
            'maxrf/10.20.8.43/corp.anjuke.com',
            'mobile/192.168.190.59/corp.anjuke.com',
            'reels/10.10.3.187/corp.anjuke.com',
        ]
        db.engine.execute("truncate table dns_apply")
        engine = create_engine(DDNS_MIGRATE_DATABASE_URI, encoding='utf-8',echo=True)
        connection = engine.connect()
        self.ddns(connection)
        connection.close()
        engine = create_engine(DNSAPPLY_MIGRATE_DATABASE_URI, encoding='utf-8',echo=True)
        connection = engine.connect()
        self.dns_migrate(connection)
        self.dns_extra_migrate(connection)
        connection.close()

    def ddns(self,connection):
        #sql = "select *  from dynamic_record where if_bind = 1 order by owner asc "
        sql = "select *  from dynamic_record where owner != '' order by owner asc "
        result = connection.execute(sql)
        for item in result:
            username = item.owner
            if '-' in item.owner:
                username = item.owner.replace('-','_')
            user_info = User.query.filter(User.name == username).first()
            if user_info:
                uid = user_info.id
                prefix = item.owner
                if item.name != "@":
                    prefix = "%s.%s"%(item.name,prefix)
                target = DnsApply(prefix= prefix,zone_id=1,type=1,value=item.value,uid=uid,approve_uid=502,content="自用域名",priority=0,status=4,deleted=0)
                db.session.add(target)
                db.session.commit()
            else:
                print("%s:找不到此用户"%username)
        connection.close()

    def dns_migrate(self,connection):#dns表
        result = connection.execute("select * from dns")
        for item in result:
            zone_info = DnsZone.query.filter(DnsZone.zone == item.suffix).first()
            if not zone_info:
                print item.suffix
                continue
            id = zone_info.id
            if item.dnstype == "A":
                dnstype = 1
            else:
                dnstype = 2

            if item.status == 0:
                status = 1#待审批
            elif item.status == 1:
                status = 4#成功
            else:
                status = 2#驳回
            ingore_key = '%s/%s/%s'%(item.prefix,item.value,zone_info.zone)
            if ingore_key in self.ignore:
                continue
            has_in = DnsApply.query.filter(and_(DnsApply.prefix == item.prefix,DnsApply.type == dnstype,DnsApply.value == item.value,DnsApply.zone_id == id, DnsApply.status == status)).first()
            if  has_in:
                continue
            user_info = User.query.filter(User.cn_name == item.username).first()
            if user_info:
                uid = user_info.id
            else:
                uid = 502
            content = str(item.details)
            pattern = '.*\.$'
            value = item.value
            if item.dnstype == "CNAME":
                if re.match(pattern,item.value):
                    replace_reg = re.compile(r'\.$')
                    value = replace_reg.sub('', item.value)
            target = DnsApply(prefix=item.prefix,zone_id=id,type=dnstype,value=value,uid=uid,approve_uid=502,content=content,priority=0,status=status,deleted=0)
            db.session.add(target)
            db.session.commit()


    def dns_extra_migrate(self,connection):#dns_extra表

        result = connection.execute("select * from dns_extra")
        for item in result:
            zone_info = DnsZone.query.filter(DnsZone.zone == item.suffix).first()
            if not zone_info:
                print '--------------2'
                print item.suffix
                continue
            id = zone_info.id
            if item.dnstype == "A":
                dnstype = 1
            elif item.dnstype == "MX":
                dnstype = 3
            elif item.dnstype == "TXT":
                dnstype = 4
            else:
                dnstype = 2
            ingore_key = '%s/%s/%s'%(item.prefix,item.value,zone_info.zone)
            if ingore_key in self.ignore:
                continue
            status = 4#成功
            has_in = DnsApply.query.filter(and_(DnsApply.prefix == item.prefix,DnsApply.type == dnstype,DnsApply.value == item.value,DnsApply.zone_id == id, DnsApply.status == status)).first()
            if has_in:
                continue
            uid = 502
            content = str(item.details)
            pattern = '.*\.$'
            value = item.value
            if item.dnstype == "CNAME":
                if re.match(pattern,item.value):
                    replace_reg = re.compile(r'\.$')
                    value = replace_reg.sub('', item.value)
            target = DnsApply(prefix=item.prefix,zone_id=id,type=dnstype,value=value,uid=uid,approve_uid=502,content=content,priority=item.priority,status=status,deleted=0)
            db.session.add(target)
            db.session.commit()