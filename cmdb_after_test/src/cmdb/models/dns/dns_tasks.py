# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer,TIMESTAMP
from application import db
import datetime

class DnsTasks(db.Model):

    __tablename__ = "dns_tasks"

    id              = Column(Integer, primary_key=True)
    dns_apply_id    = Column(Integer, nullable=False) #dns_apply表中id
    type            = Column(TINYINT, nullable=False) #0：个人域名(OFFICE) 1：公网域名(IDC外部) 2：IDC内部
    status          = Column(TINYINT, nullable=False) #任务状态 0:未运行,1:执行成功 2:执行失败
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    TYPE_OFFICE = 0
    TYPE_IDC_OUT = 1
    TYPE_IDC_IN = 2

    STATUS_FREE = 0
    STATUS_SUCCESS = 1
    STATUS_FAIL = 2

    def __init__(self,dns_apply_id,type,status):
        self.dns_apply_id = dns_apply_id
        self.type         = type
        self.status       = status
        self.created      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated      = self.created


