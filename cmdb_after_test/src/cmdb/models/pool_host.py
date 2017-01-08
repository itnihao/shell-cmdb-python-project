# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from application import db
import datetime

class PoolHost(db.Model):
    __tablename__ = "pool_host"

    id      = Column(Integer, primary_key=True)
    pool_id = Column(Integer,nullable=False,index=True)
    host_id = Column(Integer,nullable=False,index=True)
    weight    = Column(String(10),nullable=False)
    port    = Column(String(5),nullable=False)

    note    = Column(String(40),nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self,pool_id,host_id,weight=1,port=0,source=1):
        self.host_id=host_id
        self.pool_id=pool_id
        self.weight = weight
        self.port = port
        self.note=''
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated=self.created


