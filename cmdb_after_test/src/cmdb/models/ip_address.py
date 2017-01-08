# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class IpAddress(db.Model):
    __tablename__ = "ip_address"

    id        = Column(Integer, primary_key=True)
    ipv4      = Column(String(15),nullable=False,unique=True)
    flag      = Column(TINYINT(1),nullable=False,index=True)
    note      = Column(String(40),nullable=False)
    type      = Column(TINYINT(1),nullable=False,index=True) #type=1,主机   type=2,设备   type=0,default
    target_id = Column(Integer, nullable=False,index=True)
    created   = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated   = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    FLAG_AVAILABLE = 0
    FLAG_USED = 1

    TYPE_DEFAULT = 0
    TYPE_HOST = 1
    TYPE_DEVICE = 2

    def __init__(self,ipv4,flag,type = 0,target_id = 0):
        self.ipv4=ipv4
        self.flag=flag
        self.note=''
        self.type=type
        self.target_id=target_id
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated=self.created

    @property
    def flag_descri(self):
        if self.flag == 1:
           return  '已占用'
        elif self.flag == 2:
           return  '系统预留'
        else :
           return  '未占用'
