# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime


class DeviceCategory(db.Model):
    __tablename__ = "device_category"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    short_name = Column(String(30), nullable=False)
    note = Column(String(40), nullable=False)
    deleted = Column(TINYINT(1), nullable=False, index=True,server_default='0')
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, name, short_name, note,updated):
        self.name = name
        self.short_name = short_name
        self.note = note
        self.deleted = 0
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = updated



