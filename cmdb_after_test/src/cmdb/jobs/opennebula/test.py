# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../../")
from views.oca import Client
from main import CMDB_VM
from main import CMDB_HOST
from main import CMDB_VN
import urllib2
from xml.dom import minidom

# CREDENTIALS = "oneadmin:plain:password"
# ENDPOINT = "http://192.168.1.158:2633/RPC2"

CREDENTIALS = "oneadmin:plain:opennebula@YWprX29wcwo="
ENDPOINT = "http://10.10.3.56:2633/RPC2"

client = Client(CREDENTIALS, ENDPOINT)

vm_create = CMDB_VM(client)


# vm_create.deploy(152,6)
# a = vm_create.get_vm_info(152)
# print a

# host_pool = CMDB_HOST(client)
# info  =  host_pool.hostpool(client)
# print info
#used =  host_pool.hostpool(client)['mem']['usage']
# total = host_pool.hostpool(client)['mem']['total']
# print used/total

vm_network = CMDB_VN(client)
# vm_network.available_vn(client)
a = vm_network.available_vn(client)
print a
# print a
# a = vm_network.available_vn(client)
# print a
# print a
# vm_id = vm_create.create_vm(NAME = "test-01", CPU = 2, VCPU = 2, MEMORY = 2048,DISK=200,NETWORK="192.168.1.0 fixed",IMAGE_NAME="ubuntu-12.04.qcow2")
# print vm_id
# vm_create.deploy(vm_id,6)

# APC_URL = "http://192.168.1.158:4567"
# APC_AUTH = "Basic b25lYWRtaW46NWJhYTYxZTRjOWI5M2YzZjA2ODIyNTBiNmNmODMzMWI3ZWU2OGZkOA=="
# req = urllib2.Request("%s/compute/%d" % (APC_URL, 159))
# req.add_header('Authorization', APC_AUTH)
# result = urllib2.urlopen(req).read()
# xmldoc = minidom.parseString(result)
# states = xmldoc.getElementsByTagName('STATE')[0].firstChild.nodeValue
# print states
