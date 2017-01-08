# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP, SMALLINT
from application import db
import datetime

class HostIp(db.Model):
    __tablename__ = "host_ip"

    id              = Column(Integer, primary_key=True)
    host_id         = Column(Integer,nullable=False,index=True)
    net_name_id     = Column(Integer,nullable=False)
    ip_address_id   = Column(Integer,nullable=False,index=True)
    type            = Column(SMALLINT,nullable=False,index=True)
    content         = Column(String(50),nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

#type = 99:实体ip
#type = 0-98:虚拟ip端口

    def __init__(self, host_id, net_name_id,ip_address_id,type=99, content=''):
        self.host_id = host_id
        self.net_name_id = net_name_id
        self.ip_address_id = ip_address_id
        self.type = type
        self.content = content
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
