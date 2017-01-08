# -*- coding: utf-8 -*-
from sqlalchemy import *
from config import SAPPLY_DATABASE_URI
from config import MIGRATE_DATABSE_URI
from config import OPENNEBULA_DATABASE_URI
from application import db
from models.user import User
from models.apply import Apply
from models.apply_host import Apply_host
from models.host import Host
from models.pool_host import PoolHost
from xml.dom import minidom
import re

#用来迁移sapply.corp.anjuke.com平台的数据


class Sapply:
    def run(self):
        self.migirate_sapply()


    def migirate_sapply(self):
        engine1 = create_engine(SAPPLY_DATABASE_URI, encoding='utf-8',echo=False)
        connection1 = engine1.connect()
        engine2 = create_engine(MIGRATE_DATABSE_URI, encoding='utf-8',echo=False)
        connection2 = engine2.connect()
        engine3 = create_engine(OPENNEBULA_DATABASE_URI, encoding='utf-8',echo=False)
        connection3 = engine3.connect()
        a = []
        for line in open("/Users/jinbangyu/vm_id"):
            server_info = connection1.execute('select apply_id, zeus_id, applier, vm_id, create_time from `server` where vm_id != "" and vm_id= %s' %line).fetchall()
            if server_info:
                apply_id = server_info[0][0]
                zeus_id = server_info[0][1]
                applier = server_info[0][2]
                vm_id = server_info[0][3]
                created_time = server_info[0][4]


                if apply_id in a:
                    continue
                else:
                    a.append(apply_id)
                apply_info = connection1.execute('select s_id, s_num, name, status, apply_date from `apply` where id= %s' %apply_id).fetchall()
                smodel_id = apply_info[0][0]
                num = apply_info[0][1]
                content = apply_info[0][2]
                status = apply_info[0][3]
                created = apply_info[0][4]
                if status and status == 7:
                    status = 5
                if status and status ==6:
                    status = 4

                smodel_info = connection1.execute('select cpucores,memsize,disk, template from `smodel` where id = %s' %smodel_id).fetchall()
                cpu = int(smodel_info[0][0])
                mem = int(smodel_info[0][1])
                disk_info = smodel_info[0][2]
                if disk_info:
                    disk= int(re.findall(r'\d+',str(disk_info))[0])
                xml = smodel_info[0][3]
                xmldoc = minidom.parseString(xml)
                idc_info = xmldoc.getElementsByTagName('INSTANCE_TYPE')[0].firstChild.nodeValue
                if re.search('[i|I][d|D][c|C]20', idc_info):
                    idc = 2
                else:
                    idc = 1

                if re.search('ubuntu',idc_info):
                    if re.search('14.04',idc_info):
                        os = "ubuntu14.04"
                    else:
                        os = "ubuntu12.04"
                elif re.search('centos',idc_info):
                    os = "centos"
                elif re.search('redhat', idc_info):
                    os = "redhat"




                zeus_info = connection2.execute('select label from `item` where id= %s' %zeus_id).fetchall()
                hostname = zeus_info[0][0]
                host_info = Host.query.with_entities(Host.id).filter(Host.hostname == hostname).first()
                if host_info:
                    host_id = host_info.id
                    pool_info = PoolHost.query.with_entities(PoolHost.pool_id).filter(PoolHost.host_id == host_id).first()
                    if pool_info:
                        pool_id = pool_info.pool_id
                    else:
                        pool_id = 0
                else:
                    host_id = 0
                    pool_id = 0


                cmdb_user_info = User.query.with_entities(User.id).filter(User.name == applier).first()
                if cmdb_user_info:
                    applier_uid = cmdb_user_info.id
                else:
                    applier_uid = 0


                apc_info = connection3.execute('select body from `vm_pool` where oid= %s' %vm_id).fetchall()
                apc_xml = str(apc_info[0][0])
                xmldoc = minidom.parseString(apc_xml)
                apc_hostname = xmldoc.getElementsByTagName('HOSTNAME')[1].firstChild.nodeValue
                apc_info = Host.query.with_entities(Host.id).filter(Host.hostname == apc_hostname).first()
                if apc_info:
                    apc_id = apc_info.id
                else:
                    apc_id = 0


                template = {'cpu': cpu, 'mem': mem, 'disk': disk, 'os': os}
                target_apply = Apply(uid=applier_uid, approver_uid=502, pool_id=pool_id, type=2, idc=idc, num=num, status=status, template=str(template), content=content, created=created)
                db.session.add(target_apply)
                db.session.commit()

                target_apply_host = Apply_host(apply_id=target_apply.id, vm_id=vm_id, apc_id=apc_id, host_id=host_id, created=created_time)
                db.session.add(target_apply_host)
                db.session.commit()

#                print apply_id, cpu, mem, disk, hostname, applier_uid, num, content, idc, host_id, vm_id, pool_id, status, apc_id

        connection1.close()
        connection2.close()