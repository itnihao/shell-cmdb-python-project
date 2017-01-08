# -*- coding: utf-8 -*-

from sqlalchemy.schema import Column,UniqueConstraint
from sqlalchemy.types import Integer, String, TIMESTAMP, SMALLINT,DECIMAL
from application import db
import datetime

class HostLoadRatio(db.Model):
    __tablename__ = "host_load_ratio"

    id              = Column(Integer, primary_key=True)
    host_id         = Column(Integer, nullable=False)
    ratio           = Column(DECIMAL(5,2), nullable=False)
    content         = Column(String(255), nullable=False)
    created         = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    updated         = Column(TIMESTAMP, nullable=False, server_default='0000-00-00 00:00:00')
    __table_args__ = (UniqueConstraint('host_id', 'created', name='idx_host_created'),)

    def __init__(self, host_id, ratio, content='',created = created):
        self.host_id = host_id
        self.ratio = ratio
        self.content = content
        self.created = created
        self.updated = created
