# -*- coding: utf-8 -*-

import datetime
from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, Text, TIMESTAMP
from application import db


class DeviceOperationHistory(db.Model):
    __tablename__ = "device_operation_history"

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, nullable=False, index=True)
    uid = Column(Integer, nullable=False, index=True)
    content = Column(Text, nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, device_id, uid, content):
        self.device_id = device_id
        self.uid = uid
        self.content = content
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created

