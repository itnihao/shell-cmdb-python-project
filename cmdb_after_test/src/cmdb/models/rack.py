# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Rack(db.Model):
    __tablename__ ="rack"
    id              = Column(Integer, primary_key=True)
    datacenter_id   = Column(Integer,nullable=False,index=True)
    name            = Column(String(10),nullable=False,index=True)
    height          = Column(TINYINT(3),nullable=False)
    content         = Column(String(50),nullable=False)
    deleted         = Column(TINYINT(1),nullable=False,index=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, name, datacenter_id, content, height):
        self.name = name
        self.height = height
        self.datacenter_id = datacenter_id
        self.content = content
        self.deleted = 0
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
