# -*- coding: utf-8 -*-
from models.dns.dns_apply import DnsApply
from models.dns.dns_tasks import DnsTasks
from models.dns.dns_zone import DnsZone
import time
from application import db


class InsertDns:
    def run(self):
        print "=======start========="
        zone = "anjuke.com"
        apply_type = 2
        value = "aaa10.ajkdns2.com"
        uid = 502
        approve_uid = 502
        priority = 0
        content = "新增城市域名"
        apply_status = 4
        deleted = 0

        file = "/tmp/f1"
        failed = "/tmp/f2"
        f = open(file,'r')
        f1 = open(failed,'w+')
        list = f.readlines()
        created = time.strftime('%Y-%m-%d %X',time.localtime())
        updated =time.strftime('%Y-%m-%d %X',time.localtime())
        zone_info = DnsZone.query.filter(DnsZone.zone == zone).first()
        zone_id = zone_info.id
        for i in list:
            prefix=i.strip()
            dns_info = DnsApply.query.filter(DnsApply.prefix == prefix).all()
            if dns_info:
                f1.write('%s\n'%prefix)
            else:
                apply_target = DnsApply(prefix=prefix, zone_id=zone_id, type=apply_type, value=value, uid=uid, approve_uid=approve_uid, content=content, priority=priority, status=apply_status,deleted=deleted,ip_updated=0)
                db.session.add(apply_target)
                db.session.commit()
                dns_apply_id = apply_target.id
                task_type = 1
                task_status = 0
                task_target = DnsTasks(dns_apply_id=dns_apply_id, type=task_type, status=task_status)
                db.session.add(task_target)
                db.session.commit()
        f.close()
        f1.close()
        print "========end=========="