# -*- coding: utf-8 -*-
# author:郭威
# email: apanly@163.com
# QQ:364054110
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, Text, TIMESTAMP
from application import db


class DeviceIp(db.Model):
    __tablename__ = "device_ip"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False, index=True)
    net_name_id = Column(Integer, nullable=False)
    mac = Column(String(40), nullable=False)
    ip_address_id = Column(Integer, nullable=False, index=True)
    content = Column(String(40), nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


