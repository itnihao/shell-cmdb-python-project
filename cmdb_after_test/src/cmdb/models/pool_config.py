# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from application import db

class PoolConfig(db.Model):
    __tablename__ = "pool_config"

    id      = Column(Integer, primary_key=True)
    pool_id = Column(Integer,nullable=False,index=True)
    key     = Column(String(15),nullable=False)
    value   = Column(String(80),nullable=False)
    note    = Column(String(50),nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')