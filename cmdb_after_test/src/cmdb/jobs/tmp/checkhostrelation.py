# -*- coding: utf-8 -*-
'''
  此job用于检测host表和host_ip表关系是否对应正确
'''
from models.host import Host
from models.host_ip import HostIp
from views.host import _get_ip

class CheckHostRelation:
    def run(self):
        print "=============start==========="
        hosts = Host.query.filter(Host.deleted == 0).all()
        for host in hosts:
            hostip_id = []
            ip_addresses = HostIp.query.filter(HostIp.host_id == host.id).all()
            if host.primary_ip_id:
                pri_ipv4 = _get_ip(host.primary_ip_id)
                if ip_addresses:
                    for ip_address in ip_addresses:
                        if ip_address.ip_address_id:
                            hostip_id.append(ip_address.ip_address_id)
                    if host.primary_ip_id not in hostip_id:
                        print "The host has pri and Host_ip but not in Host_ip"
                        print "HostName:%s\n ID:%d\n IP:%s" %(host.hostname,host.id,pri_ipv4)
                else:
                    print "The host has pri but no host_ip"
                    print "HostName:%s\n ID:%d\n IP:%s" %(host.hostname,host.id,pri_ipv4)
            else:
                if ip_addresses:
                    print "The host has Host_ip but no pri"
                    print "HostName:%s\n ID:%d\n" %(host.hostname,host.id)
                else:
                    print "The host has no pri or Host_ip"
                    print "HostName:%s\n ID:%d\n" %(host.hostname,host.id)
        print "===========end======================="