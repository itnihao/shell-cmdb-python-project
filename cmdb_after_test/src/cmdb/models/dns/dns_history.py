# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import Integer,TIMESTAMP,Text
from application import db
import datetime

class DnsHistory(db.Model):

    __tablename__ = "dns_history"

    id              = Column(Integer, primary_key=True)
    dns_apply_id    = Column(Integer, nullable=False) #dns表中id
    status          = Column(TINYINT, nullable=False) #申请状态 0：驳回 1：通过 2：域名被删除
    content         = Column(Text,nullable=False)
    created         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False,server_default='0000-00-00 00:00:00')

    STATUS_REJECT = 0
    STATUS_PASS = 1
    STATUS_DELETE = 2

    def __init__(self,dns_apply_id,status,content = ''):
        self.dns_apply_id = dns_apply_id
        self.status       = status
        self.content      = content
        self.created      = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated      = self.created

