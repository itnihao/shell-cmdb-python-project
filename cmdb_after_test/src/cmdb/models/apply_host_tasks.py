# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class ApplyHostTasks(db.Model):
    __tablename__ = "apply_host_tasks"

    id              = Column(Integer, primary_key=True)
    uid             = Column(Integer, nullable=False)
    apply_id        = Column(Integer, nullable=False,index=True)
    pool_id         = Column(TINYINT(1), nullable=False)
    type            = Column(TINYINT(1), nullable=False)
    idc             = Column(TINYINT(1), nullable=False)
    num             = Column(Integer, nullable=False)
    template        = Column(String(255), nullable=False)
    status          = Column(TINYINT(1), nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    def __init__(self, uid, apply_id, pool_id,type,idc,num,template,status):
        self.uid = uid
        self.apply_id = apply_id
        self.pool_id = pool_id
        self.type = type
        self.idc = idc
        self.num = num
        self.template = template
        self.status = status
        self.created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated = self.created