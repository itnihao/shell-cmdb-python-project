# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Apply_host(db.Model):
    __tablename__ = "apply_host"

    id = Column(Integer, primary_key=True)
    apply_id = Column(Integer, nullable=False)
    vm_id = Column(Integer, nullable=False)
    apc_id = Column(Integer, nullable=False)
    host_id = Column(Integer, nullable=False)
    status = Column(TINYINT(1), nullable=False)
    created = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')


    PENDING  = 1
    ACTIVE = 3
    FAILD = 7

    def __init__(self, apply_id=0, vm_id=0, apc_id=0, host_id=0, status=1,created=""):
        self.apply_id = apply_id
        self.vm_id = vm_id
        self.apc_id = apc_id
        self.host_id = host_id
        self.status = status
        if created:
            self.created = created
        else:
            self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created
