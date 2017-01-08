# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, TIMESTAMP, String
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class Vm(db.Model):
    __tablename__   = "vm"

    id              = Column(Integer, primary_key=True)
    vm_id           = Column(Integer,nullable=False,index=True)
    status          = Column(TINYINT(3), nullable=False,index=True)
    content         = Column(String(50),nullable=False)
    host_id         = Column(Integer,nullable=False,index=True)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    STATUS_UNPROCESS = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2
    STATUS_NOTEXIST = 3

    def __init__(self, vm_id, status, content='', host_id=0):
        self.vm_id      = vm_id
        self.status     = status
        self.content    = content
        self.host_id    = host_id
        self.created    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated    = self.created
