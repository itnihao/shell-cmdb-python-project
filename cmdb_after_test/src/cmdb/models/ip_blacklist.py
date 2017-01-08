# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column
from sqlalchemy.types import Integer, String, TIMESTAMP
from sqlalchemy.dialects.mysql import TINYINT
from application import db
import datetime

class IpBlacklist(db.Model):
    __tablename__ = "ip_blacklist"

    id         = Column(Integer, primary_key=True)
    ip_address = Column(String(15), nullable=False)
    type       = Column(TINYINT, nullable=False) #type=1,lb-10    type=2,lb-20
    content    = Column(String(255), nullable=False)
    user_id    = Column(Integer, nullable=False)
    deleted    = Column(TINYINT, nullable=False, server_default='0')
    created    = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    updated    = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')

    def __init__(self,ip_address,type,content,user_id=0):
        self.ip_address=ip_address
        self.content=content
        self.type=type
        self.user_id=user_id
        self.deleted=0
        self.created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated=self.created


