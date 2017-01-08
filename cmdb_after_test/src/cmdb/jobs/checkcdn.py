# -*- coding: utf-8 -*-
from application import db,app
from models.dns.dns_zone import DnsZone
from sqlalchemy import or_,and_,desc
from apis.paramikolib import ParamikoLib
from models.dns.cdn import Cdn
from models.dns.cdn_details import CdnDetails
from configure.cdn import Area_List
from views.sa.dns import get_cdn
from signal import signal, SIGTERM
import os,time,atexit
DNS_PID_FILE = '/var/run/cmdb_cdn.pid'

def atexit_removepid(pid_file):
    try:
        os.remove(pid_file)
    except:
        pass
    print '---------end--------------'

class CheckCdn:
    def run(self):
        pid_file=DNS_PID_FILE
        if os.path.isfile(pid_file):
            print("The program is running")
            return 1
        else:
            try:
                signal(SIGTERM, lambda signum, stack_frame: exit(1))
                atexit.register(lambda:atexit_removepid(pid_file))
                fd=os.open(pid_file,os.O_CREAT|os.O_EXCL|os.O_RDWR)
                os.write(fd,"%s\n" % os.getpid())
                os.close(fd)
            except:
                print("Cann't get a lock file")
                return 1
        #是否需要加入防止多跑了几个Job
        print '------------start-------------'
        host = app.config.get('DNS')['outer']['host']
        dir = app.config.get('DNS')['outer']['file_dir']

        for i in range(0,5):
            file_dir = (dir + '/' + Area_List[i] + '/cdn/')
            par = ParamikoLib(host)
            par.execute('ls %s'%file_dir)
            files_txt = par.get_stdout()
            files = files_txt.split('\n')
            for file in files:
                zone_name = ''
                names = file.split('.')
                for name in names[:-1]:
                    zone_name += name + '.'
                zone_name = zone_name[:-1]
                par.execute("cat %s | grep 'CNAME'| grep -v ';'| awk '{print $1\"\t\"$4}'"%(file_dir+file))
                cons = par.get_stdout()
                lines = cons.split('\n')
                for line in lines:
                    l = line.split('\t')
                    dns_zone = DnsZone.query.filter(DnsZone.zone == zone_name).first()
                    cdn_details = CdnDetails.query.filter(and_(CdnDetails.prefix == l[0],CdnDetails.area == i,CdnDetails.zone_id == dns_zone.id)).first()
                    if not cdn_details:
                        cdn_name = get_cdn(l[1],l[0],zone_name)
                        if cdn_name:
                            cdn = Cdn.query.filter(Cdn.cdn == cdn_name).first()
                            if cdn:
                                cdn_details_target = CdnDetails(prefix=l[0],zone_id=dns_zone.id,area=i,cdn_id=cdn.id,visits=0)
                                db.session.add(cdn_details_target)
                                db.session.commit()



