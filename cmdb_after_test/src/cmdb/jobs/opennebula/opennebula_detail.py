# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("../../")
from views.oca import Client
from sqlalchemy import *
from main import CMDB_HOST
from main import CMDB_VM
from xml.dom import minidom
from config import OPENNEBULA_DATABASE_URI
from config import CREDENTIALS
from config import ENDPOINT
from config import mail_receiver
from views.functions import sendmail


engine = create_engine(OPENNEBULA_DATABASE_URI, encoding='utf-8',echo=False)
connection = engine.connect()
client = Client(CREDENTIALS, ENDPOINT)


#发送邮件的内容
host_pool = CMDB_HOST(client)
info  =  host_pool.hostpool(client)
host_number = 0
content=""
for host_data in info:
    free_mem = (int(host_data['node_info']['mem']['total']) - int(host_data['node_info']['mem']['usage']))/1024
    if free_mem <= 0:
        free_vms=0
    else:
        free_vms=free_mem/2

    host_name = host_data['node']
    running_vms = host_data['running_vms']
    host_number = host_number + 1
    content=content + "<tr>" + "<td>%s</td>"%host_name + "<td>%s</td>"%running_vms + "<td>%s</td>"%free_vms + "</tr>"
    tmp_content='''
    <style type="text/css">
        table.gridtable td {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #ffffff;
        }
        table.gridtable {
        fonts-family: verdana,arial,sans-serif;
        fonts-size:11px;
        color:#333333;
        border-width: 1px;
        border-color: #666666;
        border-collapse: collapse;
        }
        table.gridtable th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #666666;
        background-color: #dedede;
        }
    </style>
    '''
html_content=tmp_content + """
    <table class="gridtable">
        <thead>
            <tr>
            <th>宿主机</th>
            <th>运行虚拟机/个</th>
            <th>可开通(2G内存虚机/个)</th>
            </tr>
        </thead>
        <tbody>
        %s
        </tbody>
    </table>
"""%content

#获取已经上架的宿主机数量和已经开通的虚拟机数量
vm_info = CMDB_VM(client)
xml = vm_info.info()
xmldoc = minidom.parseString(xml)
b = []
for a in xmldoc.getElementsByTagName('NAME'):
    c = a.firstChild.nodeValue
    if c not in b:
        b.append(c)

title="宿主机共%s台,虚拟机%s台" %(host_number,len(b))

#发送邮件
if sendmail(title,html_content,mail_receiver):
    print "发送成功"
else:
    print "发送失败"
