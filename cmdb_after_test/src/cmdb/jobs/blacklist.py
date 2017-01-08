# -*- coding: utf-8 -*-

from pynginxconfig import NginxConfig
from application import db
from models.ip_blacklist import IpBlacklist


class Blacklist:
    def run(self):
        nc = NginxConfig()
        nc.loadf('/tmp/ngx_conf_lb_external/conf.d/deny.ip')
        print("start=========")
        for data in nc.data:
            blacklist = IpBlacklist(ip_address=data[1], type=1, content="", user_id=0)
            db.session.add(blacklist)
            db.session.commit()
            print("=======")
            print(blacklist.id)
        print("end===========")


