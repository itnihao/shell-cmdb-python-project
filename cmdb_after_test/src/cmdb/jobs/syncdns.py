# -*- coding: utf-8 -*-
from application import db, app
from models.dns.dns_zone import DnsZone
from sqlalchemy import and_
from apis.paramikolib import ParamikoLib
from models.dns.dns_apply import DnsApply
from models.user import User
from models.dns.dns_apply import get_type_num
from signal import signal, SIGTERM
import os, datetime, atexit

DNS_PID_FILE = '/var/run/cmdb_dns.pid'


def atexit_removepid(pid_file):
    try:
        os.remove(pid_file)
    except:
        pass
    print '---------end--------------'


class SyncDns:
    def run(self):
        pid_file = DNS_PID_FILE
        if os.path.isfile(pid_file):
            print("The program is running")
            return 1
        else:
            try:
                signal(SIGTERM, lambda signum, stack_frame: exit(1))
                atexit.register(lambda: atexit_removepid(pid_file))
                fd = os.open(pid_file, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.write(fd, "%s\n" % os.getpid())
                os.close(fd)
            except:
                print("Cann't get a lock file")
                return 1
        # 是否需要加入防止多跑了几个Job
        print '------------start-------------'
        dnss = app.config.get('DNS')
        admin = app.config.get('SA_UIDS')[0]

        for dns in dnss:
            host = dnss[dns]['host']
            if dns == "outer":
                file_dir = dnss[dns]['file_dir'] + '/default/'
            else:
                file_dir = dnss[dns]['file_dir'] + '/'
            par = ParamikoLib(host)
            par.execute('ls %s' % file_dir)
            files_txt = par.get_stdout()
            files = files_txt.split('\n')
            for file in files:
                domain_name = file
                if dns == "outer":
                    domain_name = file[:-8]
                dns_zone = DnsZone.query.filter(DnsZone.zone == domain_name).first()
                if dns_zone:
                    print "========" + file + "========"
                    par.execute("cat %s | grep -v ';'| grep -E '^\S+\s+A|CNAME\s+\S+$'" % (file_dir + file))
                    cons = ""
                    cons = par.get_stdout()
                    if cons != "":
                        try:
                            lines = cons.split('\n')
                            for line in lines:
                                l = line.split()
                                if l[1] != "A":
                                    l[2] = l[2][:-1]
                                    dns_apply = DnsApply.query.filter(
                                        and_(DnsApply.prefix == l[0], DnsApply.zone_id == dns_zone.id,
                                             DnsApply.deleted == DnsApply.DELETED_NO)).first()
                                    if not dns_apply:
                                        type_num = get_type_num(l[1])
                                        n = l[2].index('.')
                                        uname = l[2][:n]
                                        user = User.query.filter(and_(User.status == 0,User.name == uname)).first()
                                        if user:
                                            userid = user.id
                                        else:
                                            userid = admin
                                        dns_apply_target = DnsApply(prefix=l[0], zone_id=dns_zone.id, type=type_num,
                                                                    value=l[2], uid=userid, approve_uid=admin,
                                                                    content='自动同步添加', priority=0, status=4, deleted=0,
                                                                    ip_updated=0)
                                        db.session.add(dns_apply_target)
                                        db.session.commit()
                        except:
                            pass
