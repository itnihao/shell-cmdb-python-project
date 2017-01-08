# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
from jinja2 import Markup
import datetime

class Datacenter(db.Model):
    __tablename__ = "datacenter"
    id          = Column(Integer, primary_key=True)
    name        = Column(String(20),nullable=False, unique=True)
    short_name  = Column(String(20),nullable=False)
    address     = Column(String(80),nullable=False)
    idc_label   = Column(String(20),nullable=False)
    content     = Column(Text,nullable=False)
    deleted     = Column(TINYINT(1),nullable=False,index=True,server_default='0')
    created     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated     = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, name, short_name, address,idc_label, content):
        self.name = name
        self.short_name = short_name
        self.address= address
        self.idc_label=idc_label
        self.content=content
        self.deleted=0
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated=self.created

    @property
    def content_nr2br(self):
        return Markup(self.content.replace("\n","<br>"))
